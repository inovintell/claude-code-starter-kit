#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Stop hook validator for /setup command.
Verifies the project is fully set up before allowing the agent to finish.
"""

import json
import logging
import subprocess
import sys
from pathlib import Path

try:
    from dotenv import dotenv_values
except ImportError:
    dotenv_values = None

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "validate_setup.log"

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.FileHandler(LOG_FILE, mode="a")],
)
logger = logging.getLogger(__name__)


def check(name: str, condition: bool, fail_msg: str) -> dict:
    """Create a check result."""
    return {"name": name, "passed": condition, "message": fail_msg if not condition else "OK"}


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    cwd = hook_input.get("cwd", ".")
    logger.info(f"Validating setup in {cwd}")

    checks = []

    # 1. pyproject.toml exists
    checks.append(check("pyproject.toml", (Path(cwd) / "pyproject.toml").exists(), "Missing pyproject.toml"))

    # 2. .venv exists (uv sync ran)
    checks.append(check("Virtual env", (Path(cwd) / ".venv").exists(), "No .venv - run: uv sync"))

    # 3. .env exists
    env_path = Path(cwd) / ".env"
    checks.append(check("Env file", env_path.exists(), "No .env file - copy env.sample.txt to .env"))

    # 4. .env has no placeholder values
    if env_path.exists() and dotenv_values:
        vals = dict(dotenv_values(env_path))
        placeholders = [k for k, v in vals.items() if v and "..." in v]
        checks.append(check("Env values", len(placeholders) == 0, f"Placeholder values in: {', '.join(placeholders)}"))

    # 5. Git initialized
    try:
        r = subprocess.run(["git", "rev-parse", "--git-dir"], capture_output=True, text=True, timeout=5, cwd=cwd)
        checks.append(check("Git repo", r.returncode == 0, "Not a git repo - run: git init"))
    except Exception:
        checks.append(check("Git repo", False, "Could not check git status"))

    # 6. Required directories exist
    required_dirs = ["apps", "specs", "tests", "ai_docs"]
    missing = [d for d in required_dirs if not (Path(cwd) / d).exists()]
    checks.append(check("Directories", len(missing) == 0, f"Missing directories: {', '.join(missing)}"))

    # 7. CLAUDE.md exists
    checks.append(check("CLAUDE.md", (Path(cwd) / "CLAUDE.md").exists(), "Missing CLAUDE.md"))

    # Evaluate
    failures = [c for c in checks if not c["passed"]]

    if failures:
        reasons = "\n".join(f"- {c['name']}: {c['message']}" for c in failures)
        logger.warning(f"Setup validation failed:\n{reasons}")
        print(json.dumps({
            "result": "block",
            "reason": f"Setup incomplete. Fix these issues:\n{reasons}",
        }))
    else:
        logger.info("Setup validation passed")
        print(json.dumps({
            "result": "continue",
            "message": f"All {len(checks)} setup checks passed.",
        }))


if __name__ == "__main__":
    main()
