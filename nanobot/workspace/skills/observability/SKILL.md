---
name: observability
description: Use VictoriaLogs and VictoriaTraces MCP tools for debugging
always: true
---

# Observability Skill — Task 3

> This skill enables the agent to diagnose failures using observability data.

You have access to observability tools for querying logs and traces. Use these tools to diagnose issues in the LMS backend.

## Available Tools

| Tool | Description |
|------|-------------|
| `logs_search` | Search logs using LogsQL query |
| `logs_error_count` | Count errors per service over a time window |
| `traces_list` | List recent traces for a service |
| `traces_get` | Fetch a specific trace by ID |

## Strategy Rules

### When the user asks "What went wrong?" or "Check system health":

**Follow this investigation flow:**

1. **First** call `logs_error_count` with a fresh time window (2-5 minutes)
   - Service: "Learning Management Service"
   - Minutes: 2-5 (fresh window)

2. **If errors exist**, call `logs_search` to find specific error details:
   - Query: `_time:5m service.name:"Learning Management Service" severity:ERROR`
   - Look for: error messages, exception types, and **trace_id** values

3. **If you find a trace_id in the logs**, call `traces_get` to fetch the full trace
   - This shows the complete request flow and where it failed

4. **Summarize findings** as a coherent investigation:
   - Mention the error type found in logs
   - Reference the trace and where it failed
   - Name the affected service and operation
   - Don't dump raw JSON — explain in plain language

### When the user asks about errors or failures:

1. **First** call `logs_error_count` with the service name and time window to see if there are recent errors
2. **If errors exist**, call `logs_search` with a query like:
   - `_time:10m service.name:"Learning Management Service" severity:ERROR`
3. **If you find a trace_id in the logs**, call `traces_get` to fetch the full trace
4. **Summarize findings** concisely — don't dump raw JSON

### When the user asks about a specific request:

1. Ask for the `trace_id` if they have it
2. Call `traces_get` with the trace ID
3. Explain the span hierarchy and where any errors occurred

### Query patterns:

**Find recent errors:**
```
_time:10m service.name:"Learning Management Service" severity:ERROR
```

**Find logs for a specific trace:**
```
trace_id:<trace_id_from_logs>
```

**Find all logs from a service:**
```
_time:30m service.name:"Learning Management Service"
```

## Response Format

- Keep responses concise and focused on the issue
- Highlight key findings (error type, affected service, timestamp)
- If you found a trace, summarize the span hierarchy
- If no errors found, say so clearly

## Example Interactions

**User:** "Any errors in the last 10 minutes?"
**You:** (Call `logs_error_count` with minutes=10) → "I found X errors in the Learning Management Service in the last 10 minutes. [Details...]"

**User:** "What went wrong with my request?"
**You:** (Ask for trace_id or search recent error logs) → (Call `traces_get` or `logs_search`) → "The request failed at [span] with error: [error message]"

**User:** "Is the backend healthy?"
**You:** (Call `logs_error_count` with minutes=5) → "No errors in the last 5 minutes. The backend appears healthy."
