#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Pre-tool-use hook: blocks dangerous commands and protects sensitive files.
Reads hook input from stdin (JSON), outputs JSON decision to stdout.
"""

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR.parent.parent / "logs"
LOG_FILE = LOG_DIR / "pre_tool_use.json"

# Dangerous command patterns to block
DANGEROUS_PATTERNS = [
    r"rm\s+-rf\s+/",
    r"rm\s+-rf\s+~",
    r"rm\s+-rf\s+\.",
    r"chmod\s+-R\s+777\s+/",
    r"mkfs\.",
    r"dd\s+if=.*of=/dev/",
    r">\s*/dev/sd",
    r"find\s+.*-type\s+f\s+-delete",
    r"git\s+reset\s+--hard",
]

# Protected file patterns
PROTECTED_FILE_PATTERNS = [
    r"\.env$",
    r"\.env\.local$",
    r"\.env\.production$",
    r"credentials",
    r"secrets?\.json",
    r"\.pem$",
    r"\.key$",
]

# Allowed env file patterns
ALLOWED_ENV_PATTERNS = [
    r"\.env\.sample$",
    r"\.env\.example$",
    r"\.env\.template$",
]


def log_event(input_data, decision, reason=None):
    """Append event to log file."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_data = []
    if LOG_FILE.exists():
        try:
            log_data = json.loads(LOG_FILE.read_text())
        except (json.JSONDecodeError, ValueError):
            log_data = []

    log_data.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "tool_name": input_data.get("tool_name", "unknown"),
        "decision": decision,
        "reason": reason,
    })

    LOG_FILE.write_text(json.dumps(log_data, indent=2))


def check_bash_command(command: str) -> tuple[str, str | None]:
    """Check if a bash command is dangerous. Returns (decision, reason)."""
    for pattern in DANGEROUS_PATTERNS:
        if re.search(pattern, command):
            return "block", f"Blocked dangerous command matching pattern: {pattern}"
    return "allow", None


def check_file_access(file_path: str, tool_name: str) -> tuple[str, str | None]:
    """Check if file access should be blocked. Returns (decision, reason)."""
    # Allow reading env samples
    for pattern in ALLOWED_ENV_PATTERNS:
        if re.search(pattern, file_path):
            return "allow", None

    # Block access to protected files
    for pattern in PROTECTED_FILE_PATTERNS:
        if re.search(pattern, file_path):
            return "block", f"Blocked {tool_name} access to protected file: {file_path}"

    return "allow", None


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except json.JSONDecodeError:
        hook_input = {}

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    decision = "allow"
    reason = None

    if tool_name == "Bash":
        command = tool_input.get("command", "")
        decision, reason = check_bash_command(command)

    elif tool_name in ("Read", "Write", "Edit"):
        file_path = tool_input.get("file_path", "")
        decision, reason = check_file_access(file_path, tool_name)

    log_event(hook_input, decision, reason)

    if decision == "block":
        print(json.dumps({"decision": "block", "reason": reason}))
    else:
        print(json.dumps({}))


if __name__ == "__main__":
    main()
