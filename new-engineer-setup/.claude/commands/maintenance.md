---
allowed-tools: Read, Bash
description: Run maintenance tasks and report results
---

# Maintenance

Run maintenance tasks for the project and report results.

## Workflow

1. Update Python dependencies: `uv sync --upgrade`
2. Check for any database maintenance needs
3. Verify all services are healthy
4. Check disk usage of logs directory

## Report

Provide a summary of:
- Dependencies updated
- Maintenance tasks completed
- Any issues found
- Recommendations
