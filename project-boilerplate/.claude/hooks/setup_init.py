#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "python-dotenv",
# ]
# ///

"""
Setup hook: triggered by `claude --init`.
Installs dependencies, validates environment, reports results.
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
    logger.info(f"Step: {name}")
    try:
        result = subprocess.run(
            command, capture_output=True, text=True, timeout=120, cwd=cwd,
        )
        ok = result.returncode == 0
        logger.info(f"  {'OK' if ok else 'FAIL'}: {name}")
        if not ok:
            logger.error(f"  stderr: {result.stderr[:500]}")
        return {"step": name, "success": ok, "output": (result.stdout if ok else result.stderr)[:200]}
    except subprocess.TimeoutExpired:
        logger.error(f"  TIMEOUT: {name}")
        return {"step": name, "success": False, "output": "Timed out after 120s"}
    except FileNotFoundError as e:
        logger.error(f"  NOT FOUND: {e}")
        return {"step": name, "success": False, "output": str(e)}


def check_tool(name: str) -> dict:
    """Check if a CLI tool is available."""
    try:
        result = subprocess.run(
            ["which", name], capture_output=True, text=True, timeout=5,
        )
        found = result.returncode == 0
        return {"step": f"Check {name}", "success": found, "output": result.stdout.strip() if found else f"{name} not found"}
    except Exception:
        return {"step": f"Check {name}", "success": False, "output": "check failed"}


def check_env(cwd: str) -> dict:
    """Check if env file exists and has required vars."""
    env_path = Path(cwd) / ".env"
    if not env_path.exists():
        sample = Path(cwd) / "env.sample.txt"
        if sample.exists():
            return {"step": "Check env", "success": False, "output": "No .env file. Copy env.sample.txt to .env and fill in values."}
        return {"step": "Check env", "success": False, "output": "No .env file found."}

    if dotenv_values:
        vals = dict(dotenv_values(env_path))
        empty = [k for k, v in vals.items() if not v or v.startswith("sk-ant-...")]
        if empty:
            return {"step": "Check env", "success": False, "output": f"Empty/placeholder vars: {', '.join(empty)}"}
        return {"step": "Check env", "success": True, "output": f"{len(vals)} variables loaded"}

    return {"step": "Check env", "success": True, "output": ".env exists (dotenv not available for validation)"}


def main():
    try:
        stdin_data = sys.stdin.read()
        hook_input = json.loads(stdin_data) if stdin_data.strip() else {}
    except json.JSONDecodeError:
        hook_input = {}

    cwd = hook_input.get("cwd", ".")
    logger.info(f"Setup init in {cwd}")

    results = []

    # 1. Check required tools
    for tool in ["uv", "git", "gh"]:
        results.append(check_tool(tool))

    # 2. Install Python dependencies
    results.append(run_step("Install Python deps", ["uv", "sync"], cwd))

    # 3. Check env
    results.append(check_env(cwd))

    # 4. Ensure directories exist
    for d in ["apps", "specs", "app_review", "app_fix_reports", "scripts", "tests", "logs", "ai_docs"]:
        dir_path = Path(cwd) / d
        dir_path.mkdir(parents=True, exist_ok=True)
    results.append({"step": "Create directories", "success": True, "output": "All project directories verified"})

    # 5. Check git repo
    git_check = run_step("Check git repo", ["git", "rev-parse", "--git-dir"], cwd)
    if not git_check["success"]:
        git_check["output"] = "Not a git repo. Run: git init"
    results.append(git_check)

    passed = sum(1 for r in results if r["success"])
    total = len(results)
    logger.info(f"Setup: {passed}/{total} passed")

    output = {
        "hookSpecificOutput": {"results": results, "summary": f"{passed}/{total} checks passed"},
        "additionalContext": "\n".join(
            f"{'OK' if r['success'] else 'FAIL'}: {r['step']} - {r['output']}" for r in results
        ),
    }
    print(json.dumps(output))


if __name__ == "__main__":
    main()
