#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Post-tool-use validator: runs ruff linting on Python files after Write operations.
Returns block decision if linting fails, allowing Claude to fix issues.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "ruff_validator.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")],
)
logger = logging.getLogger(__name__)


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except json.JSONDecodeError:
        hook_input = {}
        logger.warning("Failed to parse stdin as JSON")

    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "")

    # Only check Python files
    if not file_path.endswith(".py"):
        print(json.dumps({}))
        return

    # Skip if file doesn't exist
    if not Path(file_path).exists():
        print(json.dumps({}))
        return

    logger.info(f"Running ruff check on: {file_path}")

    try:
        result = subprocess.run(
            ["ruff", "check", file_path, "--output-format", "text"],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode != 0 and result.stdout.strip():
            issues = result.stdout.strip()
            logger.warning(f"Ruff found issues:\n{issues}")
            print(json.dumps({
                "decision": "block",
                "reason": f"Ruff linting errors found:\n{issues}\n\nPlease fix these issues.",
            }))
            return

        logger.info("Ruff check passed")

    except FileNotFoundError:
        logger.info("ruff not installed, skipping validation")
    except subprocess.TimeoutExpired:
        logger.warning("ruff check timed out")
    except Exception as e:
        logger.exception(f"Unexpected error: {e}")

    print(json.dumps({}))


if __name__ == "__main__":
    main()
