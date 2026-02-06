# Claude Code Starter Kit

Two ready-to-use templates for Claude Code projects.

## `project-boilerplate/`

Copy this into any new project to get a working Claude Code setup instantly.

**Directory layout:**

```
project-boilerplate/
├── CLAUDE.md                          # Engineering rules
├── .mcp.json                          # MCP server defaults (playwright)
├── pyproject.toml                     # UV-based Python project
├── env.sample.txt                     # Environment variable template
├── .gitignore                         # Python, logs, env, IDE, Claude runtime
├── .gitattributes                     # Line endings, diff drivers
├── apps/                              # Application code
├── ai_docs/                           # Fetched documentation cache
│   └── README.md                      # URL list for /load-ai-docs
├── specs/                             # Implementation plans (/plan output)
├── app_review/                        # Code review reports (/review output)
├── app_fix_reports/                   # Fix reports (/fix output)
├── scripts/                           # Utility scripts
├── tests/                             # Test files
├── logs/                              # Runtime logs (gitignored)
└── .claude/
    ├── settings.json                  # Status line, hooks, permissions
    ├── hooks/
    │   ├── pre_tool_use.py            # Damage control
    │   ├── post_tool_use.py           # Logging
    │   └── user_prompt_submit.py      # Prompt tracking
    ├── commands/
    │   ├── plan.md                    # Create implementation plan -> specs/
    │   ├── build.md                   # Implement plan top-to-bottom
    │   ├── review.md                  # Risk-tiered code review -> app_review/
    │   ├── fix.md                     # Fix review issues -> app_fix_reports/
    │   ├── question.md                # Read-only project Q&A
    │   ├── load-ai-docs.md            # Fetch docs from URLs -> ai_docs/
    │   └── meta-prompt.md             # Create new slash commands
    ├── agents/
    │   └── docs-scraper.md            # URL -> markdown scraping agent
    ├── output-styles/                 # 11 output formatting styles
    └── status_lines/                  # Status line scripts (v1 + v4)
```

**ADW workflow:** `/plan` -> `/build` -> `/review` -> `/fix`

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
| `/meta-prompt` | Meta-prompt that creates new slash commands |
| `/onboard-candidate` | Create assessment repo + collaborator + HTML email |
| `/question` | Read-only project Q&A |
| `/reverse-goal-setting` | Skill-first goal setting framework |
| `/review-candidate` | Weighted assessment evaluation with comparison |
| `/semantic-commit` | Group changes semantically, create issue/branch/PR |
| `/sentient` | Test damage control guards |
| `/spawn-project` | Deterministic port allocation for orchestrator instances |

**Justfile recipes:**

```bash
just help          # List all recipes
just check         # Verify dependencies (claude, uv, gh, git, ruff)
just cldi          # Deterministic init (hook only, CI-friendly)
just cldii         # Agentic init (hook + analysis)
just cldit         # Interactive init (hook + agent + questions)
just tools         # /all-tools
just question "?"  # /question
just metaprompt    # /meta-prompt
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
