#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
SessionStart hook: loads environment variables from .env into the session.
Logs session start events for debugging.
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

    session_id = hook_input.get("session_id", "unknown")
    cwd = hook_input.get("cwd", ".")
    logger.info(f"Session started: {session_id} in {cwd}")

    # Load .env variables if python-dotenv is available
    env_file = Path(cwd) / ".env"
    env_vars = {}

    if dotenv_values and env_file.exists():
        env_vars = dict(dotenv_values(env_file))
        logger.info(f"Loaded {len(env_vars)} variables from {env_file}")

        # Write env vars to Claude's session env file if available
        claude_env_file = hook_input.get("claude_env_file")
        if claude_env_file:
            with open(claude_env_file, "a") as f:
                for key, value in env_vars.items():
                    if value is not None:
                        f.write(f"{key}={value}\n")
            logger.info(f"Persisted {len(env_vars)} vars to {claude_env_file}")
    else:
        logger.info("No .env file found or python-dotenv not available")

    # Output hook response
    output = {
        "hookSpecificOutput": {
            "env_loaded": len(env_vars),
            "session_id": session_id,
        }
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
