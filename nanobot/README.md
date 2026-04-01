# Nanobot Agent — Lab 8

This nanobot instance is configured for the Learning Management System (LMS) lab.

## Setup Summary (Task 1)

- **Provider:** Qwen Code API (custom OpenAI-compatible endpoint)
- **Model:** coder-model
- **MCP Tools:** LMS backend integration (9 tools)
- **Skills:**
  - `lms` — LMS-specific tool usage strategy
  - `structured-ui` — Shared UI interaction patterns

## Configuration

See `config.json` for agent and provider settings.

## Skills

- `workspace/skills/lms/SKILL.md` — LMS tool usage
- `workspace/skills/structured-ui/SKILL.md` — UI interactions
