---
allowed-tools: Read, Bash
description: Run deterministic installation and report results
---

# Install

Run the project initialization and report results. This command examines setup logs for successes and failures.

## Workflow

1. Check if `.claude/hooks/setup_init.log` exists
2. Read the log file to understand what happened during setup
3. Check if dependencies are installed:
   - `uv sync` status
   - Any other project-specific dependencies
4. Verify environment:
   - Check for `.env` file existence (don't read contents)
   - Check Python version meets requirements
   - Check for required tools (git, gh, uv)

## Report

Provide a clear summary:
- Setup steps that succeeded
- Setup steps that failed (with suggestions to fix)
- Environment status
- Next steps for the engineer
