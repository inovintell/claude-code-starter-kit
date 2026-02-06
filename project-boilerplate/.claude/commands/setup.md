---
allowed-tools: Read, Bash, Write, Edit, Glob
description: Set up the project - install deps, configure env, validate everything works
argument-hint: [interactive: true/false]
---

# Setup

Set up this project from scratch. Install dependencies, configure environment, and validate the setup is complete. The Stop hook `validate_setup.py` will verify everything before allowing completion.

## Variables

INTERACTIVE: $1

## Instructions

- Run through each setup step in order
- If INTERACTIVE is "true", ask the user for input on env configuration
- The validate_setup.py Stop hook will automatically run when you finish - it checks: pyproject.toml, .venv, .env, git repo, directories, CLAUDE.md
- If validation fails, fix the issues before stopping

## Workflow

1. **Check prerequisites**
   ```bash
   which uv && echo "uv: OK" || echo "uv: MISSING - install from https://docs.astral.sh/uv/"
   which git && echo "git: OK" || echo "git: MISSING"
   which gh && echo "gh: OK" || echo "gh: MISSING - install from https://cli.github.com/"
   ```

2. **Initialize git** (if not already a repo)
   ```bash
   git rev-parse --git-dir 2>/dev/null || git init
   ```

3. **Install Python dependencies**
   ```bash
   uv sync
   ```

4. **Configure environment**
   - Check if `.env` exists
   - If not, copy `env.sample.txt` to `.env`
   - If INTERACTIVE is "true":
     - Read `.env` and identify placeholder values (containing `...`)
     - Ask the user to provide real values for each placeholder
     - Update `.env` with provided values
   - If INTERACTIVE is not "true":
     - Just copy the sample and note which values need to be filled in

5. **Ensure project directories exist**
   ```bash
   mkdir -p apps specs app_review app_fix_reports scripts tests logs ai_docs
   ```

6. **Verify CLAUDE.md exists**
   - If missing, warn the user

7. **Run a quick smoke test**
   ```bash
   uv run python -c "import pydantic; print(f'pydantic {pydantic.__version__}')"
   uv run python -c "from dotenv import load_dotenv; print('dotenv OK')"
   ```

## Report

Provide a setup summary:

```
Project Setup Complete
======================
Python deps:    [installed / failed]
Environment:    [configured / needs values]
Git repo:       [initialized / already existed]
Directories:    [all present]
Smoke test:     [passed / failed]

Next steps:
- [any remaining actions]
```
