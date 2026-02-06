#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
UserPromptSubmit hook: logs user prompts and stores last prompt for status line.
"""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_DIR = SCRIPT_DIR.parent.parent / "logs"
LOG_FILE = LOG_DIR / "user_prompt_submit.json"
DATA_DIR = SCRIPT_DIR.parent / "data" / "sessions"


def log_prompt(hook_input):
    """Log user prompt to log file."""
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    log_data = []
    if LOG_FILE.exists():
        try:
            log_data = json.loads(LOG_FILE.read_text())
        except (json.JSONDecodeError, ValueError):
            log_data = []

    log_data.append({
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "session_id": hook_input.get("session_id", "unknown"),
        "prompt": hook_input.get("prompt", ""),
    })

    LOG_FILE.write_text(json.dumps(log_data, indent=2))


def store_last_prompt(hook_input):
    """Store last prompt in session data for status line display."""
    session_id = hook_input.get("session_id", "unknown")
    prompt = hook_input.get("prompt", "")

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    session_file = DATA_DIR / f"{session_id}.json"

    session_data = {}
    if session_file.exists():
        try:
            session_data = json.loads(session_file.read_text())
        except (json.JSONDecodeError, ValueError):
            session_data = {}

    prompts = session_data.get("prompts", [])
    prompts.append(prompt)
    session_data["prompts"] = prompts
    session_data["last_updated"] = datetime.now(timezone.utc).isoformat()

    session_file.write_text(json.dumps(session_data, indent=2))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-only", action="store_true")
    parser.add_argument("--store-last-prompt", action="store_true")
    args = parser.parse_args()

    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data)
    except json.JSONDecodeError:
        hook_input = {}

    log_prompt(hook_input)

    if args.store_last_prompt:
        store_last_prompt(hook_input)

    print(json.dumps({}))


if __name__ == "__main__":
    main()
