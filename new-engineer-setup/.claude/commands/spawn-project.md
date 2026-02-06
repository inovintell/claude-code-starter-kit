---
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
description: Spawn orchestrator instances with deterministic ports per project/repository
argument-hint: [project-path-or-alias] [instance-number]
model: haiku
---

# spawn-project

Spawns orchestrator instances (backend + frontend) using a registry-based port allocation. Ports are explicitly assigned per project in this prompt file, guaranteeing no collisions. When adding a new project, this prompt file must be modified.

## Variables

PROJECT_INPUT: $1
INSTANCE_NUMBER: $2
ORCHESTRATOR_DIR: /Users/clazz/GitHub/tactical-agentic-coding/orchestrator-agent-with-adws/apps/orchestrator_3_stream

## Port Registry

Each project gets a base port with 10 ports reserved (5 instances x 2 ports each).
Format: `base_port + (instance - 1) * 2` = backend, `+1` = frontend

| Alias | Path | Base Port | Inst 1 (BE/FE) | Inst 2 (BE/FE) | Inst 3 (BE/FE) |
|-------|------|-----------|----------------|----------------|----------------|
| example-project | /Users/clazz/GitHub/example-project | 9010 | 9010/9011 | 9012/9013 | 9014/9015 |

**Next available base port: 9020**

## Caddy Reverse Proxy

Aliases like `example-project-1.localhost` are configured in:
`~/.config/caddy/Caddyfile`

When adding a new project, update BOTH files.

## Workflow

1. Parse the Port Registry table above to get project mappings

2. Resolve `PROJECT_INPUT`:
   - If not provided, list all registered projects with aliases and prompt user to select
   - If provided, match against:
     - **Named instance format** (e.g., "example-project-1"):
       - Parse as `<alias>-<instance_number>`
       - Resolve alias, extract instance (overrides INSTANCE_NUMBER argument)
     - Full path (exact match)
     - Alias (e.g., "example-project")
     - Partial path match (last path component)
   - **If no match found**: Offer to register the new project by editing this prompt file:
     - Assign next available base port
     - Add row to Port Registry table
     - Update "Next available base port"
     - Then proceed with spawn

3. Default `INSTANCE_NUMBER` to 1 if not provided. Validate it's between 1-5.

4. Calculate ports from registry:
   ```
   backend_port = base_port + (instance - 1) * 2
   frontend_port = backend_port + 1
   ```

5. Display the port allocation:
   ```
   Project: <resolved_project_path> (<alias>)
   Instance: <INSTANCE_NUMBER>
   Backend Port: <backend_port>
   Frontend Port: <frontend_port>
   ```

6. Check if ports are already in use:
   ```bash
   lsof -ti:<backend_port> && echo "Backend port in use"
   lsof -ti:<frontend_port> && echo "Frontend port in use"
   ```
   - If in use, ask user whether to kill existing processes or abort

7. Ensure Caddy reverse proxy is running:
   ```bash
   if pgrep -x caddy > /dev/null 2>&1; then
     caddy reload --config ~/.config/caddy/Caddyfile 2>&1
   else
     caddy start --config ~/.config/caddy/Caddyfile 2>&1
   fi
   ```
   - If Caddy fails to start, warn the user but continue (direct ports still work)

8. Start the backend server in background:
   ```bash
   cd <ORCHESTRATOR_DIR>
   BACKEND_PORT=<backend_port> \
   FRONTEND_PORT=<frontend_port> \
   CORS_ORIGINS="http://127.0.0.1:<frontend_port>,http://localhost:<frontend_port>,http://<alias>-<instance>.localhost" \
   ORCHESTRATOR_WORKING_DIR=<project_path> \
   ./start_be.sh --cwd <project_path> &
   ```

9. Start the frontend server in background:
   ```bash
   cd <ORCHESTRATOR_DIR>
   FRONTEND_PORT=<frontend_port> \
   VITE_API_BASE_URL=http://127.0.0.1:<backend_port> \
   VITE_WEBSOCKET_URL=ws://127.0.0.1:<backend_port>/ws \
   ./start_fe.sh &
   ```

10. Wait 3 seconds and verify both services started successfully

11. Open browser tab with frontend URL:
   ```bash
   open "http://<alias>-<instance>.localhost"
   ```

## Report

After execution, provide:

```
Orchestrator Instance Spawned
==============================
Project:      <project_path> (<alias>)
Instance:     <INSTANCE_NUMBER>

Backend:      http://127.0.0.1:<backend_port>
Frontend:     http://<alias>-<instance>.localhost
              http://127.0.0.1:<frontend_port>
WebSocket:    ws://127.0.0.1:<backend_port>/ws

Status: [Running | Failed]
```

Stop commands:
```bash
kill $(lsof -ti:<backend_port>)   # Stop backend
kill $(lsof -ti:<frontend_port>)  # Stop frontend
```
