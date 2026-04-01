# MCP Observability Server

MCP server providing observability tools for VictoriaLogs and VictoriaTraces.

## Tools

- `logs_search` — Search logs using LogsQL query
- `logs_error_count` — Count errors per service over a time window
- `traces_list` — List recent traces for a service
- `traces_get` — Fetch a specific trace by ID

## Environment Variables

- `VICTORIALOGS_URL` — VictoriaLogs HTTP API URL (default: `http://victorialogs:9428`)
- `VICTORIATRACES_URL` — VictoriaTraces Jaeger API URL (default: `http://victoriatraces:10428`)

## Usage

```bash
python -m mcp_obs
```
