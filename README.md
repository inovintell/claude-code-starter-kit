# Claude Code Starter Kit

Two ready-to-use templates for Claude Code projects.

## `project-boilerplate/`

Copy this into any new project to get a working Claude Code setup instantly.

**What's included:**

- `CLAUDE.md` — Engineering rules (no mocking, pydantic over dicts, UV only, ephemeral tests)
- `.claude/settings.json` — Status line, PreToolUse/PostToolUse hooks, permission deny/ask lists
- `.claude/hooks/` — Damage control (`pre_tool_use.py`), logging (`post_tool_use.py`), prompt tracking (`user_prompt_submit.py`)
- `.claude/status_lines/` — Two status line scripts (basic v1 + advanced v4 with agent name/prompts/extras)
- `.claude/output-styles/` — 11 output styles (ultra-concise, bullet-points, genui, html-structured, markdown, observable-tools-diffs, table-based, tts-summary, yaml-structured)
- `.claude/commands/question.md` — Read-only project Q&A command
- `pyproject.toml` — UV-based Python project with pydantic, rich, python-dotenv
- `.gitignore` — Python, env files, logs, IDE, Claude Code runtime data

**Usage:**

```bash
cp -r project-boilerplate/ ~/my-new-project/
cd ~/my-new-project
uv sync
```

## `new-engineer-setup/`

Onboarding toolkit for new engineers. Combines deterministic hooks with agentic commands and validation scripting.

**Hooks & Validators:**

- `session_start.py` — Loads `.env` into Claude Code session
- `setup_init.py` — Runs `uv sync` and project-specific init steps on `claude --init`
- `validators/bash_validator.py` — Blocks dangerous bash patterns (PreToolUse)
- `validators/ruff_validator.py` — Lints Python on Write (PostToolUse)
- `validators/validate_new_file.py` — Verifies file creation (Stop hook)
- `validators/validate_file_contains.py` — Verifies file content requirements (Stop hook)

**Commands (13 total, `-` normalized):**

| Command | Purpose |
|---------|---------|
| `/all-tools` | List all available tools with signatures |
| `/biweekly` | Generate HTML progress report from GitHub issues/PRs |
| `/install` | Deterministic setup verification |
| `/load-ai-docs` | Fetch documentation URLs into local markdown |
| `/maintenance` | Dependency updates and health checks |
| `/onboard-candidate` | Create assessment repo + collaborator + HTML email |
| `/question` | Read-only project Q&A |
| `/reverse-goal-setting` | Skill-first goal setting framework |
| `/review-candidate` | Weighted assessment evaluation with comparison |
| `/semantic-commit` | Group changes semantically, create issue/branch/PR |
| `/sentient` | Test damage control guards |
| `/spawn-project` | Deterministic port allocation for orchestrator instances |
| `/t-metaprompt-workflow` | Meta-prompt that creates new slash commands |

**Justfile recipes:**

```bash
just help          # List all recipes
just check         # Verify dependencies (claude, uv, gh, git, ruff)
just cldi          # Deterministic init (hook only, CI-friendly)
just cldii         # Agentic init (hook + analysis)
just cldit         # Interactive init (hook + agent + questions)
just tools         # /all-tools
just question "?"  # /question
just commit        # /semantic-commit
just biweekly      # /biweekly
just load-docs     # /load-ai-docs
just spawn proj    # /spawn-project
```

## Prerequisites

- [Claude Code](https://docs.anthropic.com/en/docs/claude-code) CLI
- [Astral UV](https://docs.astral.sh/uv/) for Python
- [just](https://github.com/casey/just) command runner
- [gh](https://cli.github.com/) GitHub CLI
