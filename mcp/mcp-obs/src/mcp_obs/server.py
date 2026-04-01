"""MCP server for observability tools (VictoriaLogs and VictoriaTraces)."""

import asyncio
import json
import os
from typing import Any

import httpx
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import TextContent, Tool
from pydantic import BaseModel, Field


class LogsSearchParams(BaseModel):
    query: str = Field(description="LogsQL query string")
    limit: int = Field(default=100, description="Max number of log entries to return")


class LogsErrorCountParams(BaseModel):
    service: str = Field(default="Learning Management Service", description="Service name")
    minutes: int = Field(default=60, description="Time window in minutes")


class TracesListParams(BaseModel):
    service: str = Field(default="Learning Management Service", description="Service name")
    limit: int = Field(default=20, description="Max number of traces to return")


class TracesGetParams(BaseModel):
    trace_id: str = Field(description="Trace ID to fetch")


ToolPayload = BaseModel


async def _text(data: Any) -> list[TextContent]:
    """Convert data to text content."""
    if isinstance(data, BaseModel):
        payload = data.model_dump()
    elif isinstance(data, (list, tuple)):
        payload = [item.model_dump() if isinstance(item, BaseModel) else item for item in data]
    else:
        payload = data
    return [TextContent(type="text", text=json.dumps(payload, ensure_ascii=False, indent=2))]


def create_server() -> Server:
    """Create the observability MCP server."""
    server = Server("mcp-obs")

    # VictoriaLogs URL
    victorialogs_url = os.environ.get("VICTORIALOGS_URL", "http://victorialogs:9428")
    # VictoriaTraces URL
    victoriatraces_url = os.environ.get("VICTORIATRACES_URL", "http://victoriatraces:10428")

    @server.list_tools()
    async def list_tools() -> list[Tool]:
        return [
            Tool(
                name="logs_search",
                description="Search logs using LogsQL query. Returns structured log entries.",
                inputSchema=LogsSearchParams.model_json_schema(),
            ),
            Tool(
                name="logs_error_count",
                description="Count errors per service over a time window.",
                inputSchema=LogsErrorCountParams.model_json_schema(),
            ),
            Tool(
                name="traces_list",
                description="List recent traces for a service.",
                inputSchema=TracesListParams.model_json_schema(),
            ),
            Tool(
                name="traces_get",
                description="Fetch a specific trace by ID.",
                inputSchema=TracesGetParams.model_json_schema(),
            ),
        ]

    @server.call_tool()
    async def call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                if name == "logs_search":
                    params = LogsSearchParams.model_validate(arguments or {})
                    # VictoriaLogs LogsQL API
                    url = f"{victorialogs_url}/select/logsql/query"
                    resp = await client.post(
                        url,
                        data={"query": params.query, "limit": params.limit},
                    )
                    resp.raise_for_status()
                    # Parse line-delimited JSON
                    lines = resp.text.strip().split("\n")
                    results = []
                    for line in lines:
                        if line.strip():
                            try:
                                results.append(json.loads(line))
                            except json.JSONDecodeError:
                                results.append({"raw": line})
                    return await _text({"entries": results, "count": len(results)})

                elif name == "logs_error_count":
                    params = LogsErrorCountParams.model_validate(arguments or {})
                    # Query for errors in time window
                    query = f'_time:{params.minutes}m service.name:"{params.service}" severity:ERROR'
                    url = f"{victorialogs_url}/select/logsql/query"
                    resp = await client.post(
                        url,
                        data={"query": query, "limit": 1000},
                    )
                    resp.raise_for_status()
                    lines = resp.text.strip().split("\n")
                    error_count = len([l for l in lines if l.strip()])
                    return await _text({
                        "service": params.service,
                        "time_window_minutes": params.minutes,
                        "error_count": error_count,
                    })

                elif name == "traces_list":
                    params = TracesListParams.model_validate(arguments or {})
                    # VictoriaTraces Jaeger-compatible API
                    url = f"{victoriatraces_url}/select/jaeger/api/traces"
                    resp = await client.get(
                        url,
                        params={"service": params.service, "limit": params.limit},
                    )
                    resp.raise_for_status()
                    data = resp.json()
                    return await _text(data)

                elif name == "traces_get":
                    params = TracesGetParams.model_validate(arguments or {})
                    url = f"{victoriatraces_url}/select/jaeger/api/traces/{params.trace_id}"
                    resp = await client.get(url)
                    resp.raise_for_status()
                    data = resp.json()
                    return await _text(data)

                else:
                    return [TextContent(type="text", text=f"Unknown tool: {name}")]

        except Exception as exc:
            return [TextContent(type="text", text=f"Error: {type(exc).__name__}: {exc}")]

    _ = list_tools, call_tool
    return server


async def main() -> None:
    """Run the MCP server."""
    server = create_server()
    async with stdio_server() as (read_stream, write_stream):
        init_options = server.create_initialization_options()
        await server.run(read_stream, write_stream, init_options)


if __name__ == "__main__":
    asyncio.run(main())
