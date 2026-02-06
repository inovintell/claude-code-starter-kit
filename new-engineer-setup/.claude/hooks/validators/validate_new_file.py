#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Stop hook validator: verifies a new file was created in a specified directory.
Uses git status + filesystem checks for detection.

Usage in settings.json:
  "command": "uv run .claude/hooks/validators/validate_new_file.py -d specs -e .md"
"""

import argparse
import json
import logging
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "validate_new_file.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")],
)
logger = logging.getLogger(__name__)


def get_git_untracked_files(directory: str, extension: str) -> list[str]:
    """Get untracked or newly added files from git status."""
    try:
        result = subprocess.run(
            ["git", "status", "--porcelain", directory],
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode != 0:
            return []

        files = []
        for line in result.stdout.strip().split("\n"):
            if not line:
                continue
            status = line[:2]
            file_path = line[3:].strip()
            # '??' = untracked, 'A ' = added
            if status in ("??", "A ") and file_path.endswith(extension):
                files.append(file_path)
        return files
    except Exception:
        return []


def get_recent_files(directory: str, extension: str, max_age_minutes: int) -> list[str]:
    """Get files modified within the time window."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return []

    now = datetime.now(timezone.utc).timestamp()
    max_age_seconds = max_age_minutes * 60
    recent = []

    for f in dir_path.rglob(f"*{extension}"):
        age = now - f.stat().st_mtime
        if age <= max_age_seconds:
            recent.append(str(f))

    return recent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=".")
    parser.add_argument("-e", "--extension", default=".py")
    parser.add_argument("--max-age", type=int, default=5, help="Max age in minutes")
    args = parser.parse_args()

    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    logger.info(f"Validating new file in {args.directory} with extension {args.extension}")

    # Check git status
    git_files = get_git_untracked_files(args.directory, args.extension)

    # Check recent filesystem changes
    recent_files = get_recent_files(args.directory, args.extension, args.max_age)

    # Combine results
    all_new = set(git_files) | set(recent_files)

    if all_new:
        logger.info(f"Found new files: {all_new}")
        print(json.dumps({
            "result": "continue",
            "message": f"Found {len(all_new)} new file(s): {', '.join(sorted(all_new))}",
        }))
    else:
        reason = f"No new {args.extension} files found in {args.directory}/ within the last {args.max_age} minutes."
        logger.warning(reason)
        print(json.dumps({
            "result": "block",
            "reason": reason,
        }))


if __name__ == "__main__":
    main()
