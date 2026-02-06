#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Post-tool-use hook: logs tool execution results.
Reads hook input from stdin (JSON), appends to log file.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR.parent.parent / "logs"
LOG_FILE = LOG_DIR / "post_tool_use.json"


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except json.JSONDecodeError:
        hook_input = {}

    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_data = []
    if LOG_FILE.exists():
        try:
            log_data = json.loads(LOG_FILE.read_text())
        except (json.JSONDecodeError, ValueError):
            log_data = []

    log_data.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_name": hook_input.get("tool_name", "unknown"),
        "hook_event_name": hook_input.get("hook_event_name", "PostToolUse"),
    })

    LOG_FILE.write_text(json.dumps(log_data, indent=2))

    # Always allow - this is just logging
    print(json.dumps({}))


if __name__ == "__main__":
    main()
