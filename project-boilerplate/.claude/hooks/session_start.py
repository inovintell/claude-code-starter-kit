#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
SessionStart hook: loads .env into the Claude Code session.
"""

import json
import logging
import sys
from pathlib import Path

try:
    from dotenv import dotenv_values
except ImportError:
    dotenv_values = None

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "session_start.log"

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
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    cwd = hook_input.get("cwd", ".")
    session_id = hook_input.get("session_id", "unknown")
    logger.info(f"Session started: {session_id} in {cwd}")

    env_file = Path(cwd) / ".env"
    loaded = 0

    if dotenv_values and env_file.exists():
        env_vars = dict(dotenv_values(env_file))
        claude_env_file = hook_input.get("claude_env_file")
        if claude_env_file:
            with open(claude_env_file, "a") as f:
                for key, value in env_vars.items():
                    if value is not None:
                        f.write(f"{key}={value}\n")
            loaded = len(env_vars)
            logger.info(f"Loaded {loaded} vars from .env")

    print(json.dumps({"hookSpecificOutput": {"env_loaded": loaded, "session_id": session_id}}))


if __name__ == "__main__":
    main()
