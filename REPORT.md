# Lab 8 — Report

Paste your checkpoint evidence below. Add screenshots as image files in the repo and reference them with `![description](path)`.

## Task 1A — Bare agent

### Question 1: "What is the agentic loop?"

**Answer:**
The agentic loop is the fundamental cycle that autonomous AI agents follow to accomplish tasks. It's the core reasoning and action pattern that enables agents to work independently toward goals.

**The Basic Loop:**

1. **Perceive** — Gather information about the current state (read files, check outputs, observe environment)
2. **Reason/Plan** — Analyze the situation, decide what to do next, form a plan or sub-goal
3. **Act** — Execute an action using available tools (run commands, write files, make API calls, send messages)
4. **Observe** — Collect feedback from the action's result (success, error, output)
5. **Repeat** — Continue the loop until the goal is achieved or a stopping condition is met

**Why It Matters:**

- **Autonomy** — Agents can work without constant human guidance
- **Adaptability** — Agents adjust based on feedback and changing conditions
- **Complex task completion** — Breaking large goals into iterative steps
- **Self-correction** — Learning from mistakes and trying alternative approaches

### Question 2: "What labs are available in our LMS?"

**Answer:**
The agent explored the workspace and found:

**Lab 8 — The Agent is the Interface**

Required Tasks:

1. Task 1: Set Up the Agent — install nanobot, configure Qwen API, add MCP tools, write skill prompt
2. Task 2: Deploy and Connect a Web Client — Dockerize nanobot, add WebSocket channel + Flutter chat UI
3. Task 3: Give the Agent New Eyes — explore observability data, write log/trace MCP tools
4. Task 4: Diagnose a Failure and Make the Agent Proactive — investigate a failure, schedule in-chat health checks, fix a planted bug

Optional Tasks:

1. Task 1: Add a Telegram Bot Client — same agent, different interface

**LMS System Components:**

- Backend: FastAPI application with routers for items, interactions, and learners
- Database: PostgreSQL with seeded data
- Frontend: React dashboard and Flutter web chat UI
- Infrastructure: Docker Compose with Caddy reverse proxy, pgAdmin, and observability tools

> **Note:** At this stage, the agent has no live LMS backend access. It answers based on local file exploration only.

## Task 1B — Agent with LMS tools

### Question 1: "What labs are available?"

**Answer:**
Here are the available labs:

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. lab-08

> **Note:** The agent now uses MCP tools to fetch real data from the LMS backend, not just local file exploration.

### Question 2: "Is the LMS backend healthy?"

**Answer:**
Yes, the LMS backend is healthy. It currently has 56 items in the system.

### MCP Tools Registered

The agent connected to the MCP server and registered 9 tools:

- `mcp_lms_lms_health` — Check backend health
- `mcp_lms_lms_labs` — List available labs
- `mcp_lms_lms_learners` — Get learner information
- `mcp_lms_lms_pass_rates` — Get pass rates for labs
- `mcp_lms_lms_timeline` — Get submission timeline
- `mcp_lms_lms_groups` — Get group information
- `mcp_lms_lms_top_learners` — Get top learners
- `mcp_lms_lms_completion_rate` — Get completion rate
- `mcp_lms_lms_sync_pipeline` — Trigger ETL sync

## Task 1C — Skill prompt

### Question: "Show me the scores" (without specifying a lab)

**Answer:**
The agent responded by first calling `lms_labs` to get the list of available labs, then asked for clarification:

"Here are the available labs. Which lab would you like to see scores for?

1. Lab 01 – Products, Architecture & Roles
2. Lab 02 — Run, Fix, and Deploy a Backend Service
3. Lab 03 — Backend API: Explore, Debug, Implement, Deploy
4. Lab 04 — Testing, Front-end, and AI Agents
5. Lab 05 — Data Pipeline and Analytics Dashboard
6. Lab 06 — Build Your Own Agent
7. Lab 07 — Build a Client with an AI Coding Agent
8. Lab 08 — lab-08

Please let me know which lab you'd like to see the pass rates for!"

### Skill Prompt Behavior

The LMS skill prompt successfully teaches the agent to:

1. **Detect missing lab parameter** — When asked about scores without a lab name
2. **Call `lms_labs` first** — To get available options
3. **Present choices** — List all labs with their titles
4. **Wait for user selection** — Before calling lab-specific tools

This follows the strategy defined in `workspace/skills/lms/SKILL.md`.

## Task 2A — Deployed agent

<!-- Paste a short nanobot startup log excerpt showing the gateway started inside Docker -->

## Task 2B — Web client

<!-- Screenshot of a conversation with the agent in the Flutter web app -->

## Task 3A — Structured logging

<!-- Paste happy-path and error-path log excerpts, VictoriaLogs query screenshot -->

## Task 3B — Traces

<!-- Screenshots: healthy trace span hierarchy, error trace -->

## Task 3C — Observability MCP tools

<!-- Paste agent responses to "any errors in the last hour?" under normal and failure conditions -->

## Task 4A — Multi-step investigation

<!-- Paste the agent's response to "What went wrong?" showing chained log + trace investigation -->

## Task 4B — Proactive health check

<!-- Screenshot or transcript of the proactive health report that appears in the Flutter chat -->

## Task 4C — Bug fix and recovery

<!-- 1. Root cause identified
     2. Code fix (diff or description)
     3. Post-fix response to "What went wrong?" showing the real underlying failure
     4. Healthy follow-up report or transcript after recovery -->
