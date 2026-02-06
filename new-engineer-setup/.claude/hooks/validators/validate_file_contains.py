#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Stop hook validator: verifies file content requirements.
Finds newest file in directory and checks for required strings.

Usage in settings.json:
  "command": "uv run .claude/hooks/validators/validate_file_contains.py -d specs -e .md --contains 'Requirements' --contains 'Timeline'"
"""

import argparse
import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "validate_file_contains.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")],
)
logger = logging.getLogger(__name__)


def find_newest_file(directory: str, extension: str, max_age_minutes: int) -> Path | None:
    """Find the newest file with the given extension in directory."""
    dir_path = Path(directory)
    if not dir_path.exists():
        return None

    now = datetime.now(timezone.utc).timestamp()
    max_age_seconds = max_age_minutes * 60

    newest = None
    newest_mtime = 0

    for f in dir_path.rglob(f"*{extension}"):
        mtime = f.stat().st_mtime
        age = now - mtime
        if age <= max_age_seconds and mtime > newest_mtime:
            newest = f
            newest_mtime = mtime

    return newest


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", default=".")
    parser.add_argument("-e", "--extension", default=".md")
    parser.add_argument("--max-age", type=int, default=5, help="Max age in minutes")
    parser.add_argument("--contains", action="append", dest="required_strings", default=[])
    args = parser.parse_args()

    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    logger.info(f"Validating file content in {args.directory}")

    newest = find_newest_file(args.directory, args.extension, args.max_age)

    if not newest:
        reason = f"No recent {args.extension} files found in {args.directory}/"
        logger.warning(reason)
        print(json.dumps({"result": "block", "reason": reason}))
        return

    logger.info(f"Checking newest file: {newest}")
    content = newest.read_text()

    missing = []
    for required in args.required_strings:
        if required not in content:
            missing.append(required)

    if missing:
        reason = f"File {newest} is missing required content: {', '.join(missing)}"
        logger.warning(reason)
        print(json.dumps({"result": "block", "reason": reason}))
    else:
        logger.info("All required strings found")
        print(json.dumps({
            "result": "continue",
            "message": f"File {newest} contains all required content.",
        }))


if __name__ == "__main__":
    main()
