#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Pre-tool-use validator for Bash commands.
Blocks dangerous patterns before execution.
"""

import json
import logging
import re
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "bash_validator.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")],
)
logger = logging.getLogger(__name__)

# Dangerous command patterns
BLOCKED_PATTERNS = [
    (r"rm\s+-rf\s+/", "Recursive delete from root"),
    (r"rm\s+-rf\s+~", "Recursive delete from home"),
    (r"rm\s+-rf\s+\.\s", "Recursive delete from current dir"),
    (r"chmod\s+-R\s+777\s+/", "World-writable permissions on system"),
    (r"mkfs\.", "Filesystem format"),
    (r"dd\s+if=.*of=/dev/", "Direct disk write"),
    (r">\s*/dev/sd", "Redirect to disk device"),
    (r"find\s+.*-type\s+f\s+-delete", "Mass file deletion"),
    (r"curl.*\|\s*(?:ba)?sh", "Pipe curl to shell"),
    (r"wget.*\|\s*(?:ba)?sh", "Pipe wget to shell"),
]


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except json.JSONDecodeError:
        hook_input = {}
        logger.warning("Failed to parse stdin as JSON")

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    logger.info(f"Checking command: {command[:100]}")

    for pattern, description in BLOCKED_PATTERNS:
        if re.search(pattern, command):
            reason = f"BLOCKED: {description} (pattern: {pattern})"
            logger.warning(reason)
            print(json.dumps({"decision": "block", "reason": reason}))
            return

    logger.info("Command allowed")
    print(json.dumps({}))


if __name__ == "__main__":
    main()
