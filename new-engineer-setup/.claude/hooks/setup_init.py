#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

"""
Setup hook: triggered by `claude --init`.
Installs dependencies, initializes database, sets environment variables.
Customize the STEPS list below for your project.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "setup_init.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")],
)
logger = logging.getLogger(__name__)


def run_step(name: str, command: list[str], cwd: str = ".") -> dict:
    """Run a setup step and return result."""
    logger.info(f"Running step: {name}")
    try:
        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,
            cwd=cwd,
        )
        success = result.returncode == 0
        logger.info(f"  {'SUCCESS' if success else 'FAILED'}: {name}")
        if not success:
            logger.error(f"  stderr: {result.stderr[:500]}")
        return {
            "step": name,
            "success": success,
            "output": result.stdout[:200] if success else result.stderr[:200],
        }
    except subprocess.TimeoutExpired:
        logger.error(f"  TIMEOUT: {name}")
        return {"step": name, "success": False, "output": "Timed out after 120s"}
    except FileNotFoundError:
        logger.error(f"  NOT FOUND: {command[0]}")
        return {"step": name, "success": False, "output": f"{command[0]} not found"}


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    cwd = hook_input.get("cwd", ".")
    logger.info(f"Setup init started in {cwd}")

    # Define setup steps - customize these for your project
    steps = [
        ("Install Python dependencies", ["uv", "sync"]),
        # ("Install frontend dependencies", ["npm", "install"]),
        # ("Run database migrations", ["uv", "run", "python", "-m", "app.db.migrate"]),
    ]

    results = []
    for name, command in steps:
        results.append(run_step(name, command, cwd))

    successes = sum(1 for r in results if r["success"])
    failures = len(results) - successes

    logger.info(f"Setup complete: {successes} passed, {failures} failed")

    output = {
        "hookSpecificOutput": {
            "results": results,
            "summary": f"{successes}/{len(results)} steps passed",
        },
        "additionalContext": f"Setup completed with {successes}/{len(results)} steps passing.",
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
