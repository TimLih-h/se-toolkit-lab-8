# Stage 1: build
ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}astral/uv:python3.14-bookworm-slim AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app/nanobot

# Copy nanobot project files
COPY pyproject.toml ./
COPY entrypoint.py ./
COPY config.json ./

# Install base nanobot-ai dependency
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system "nanobot-ai @ https://github.com/HKUDS/nanobot/archive/e7d371ec1e6531b28898ec2c869ef338e8dd46ec.zip"

# Copy and install workspace dependencies
COPY ../mcp/mcp-lms /app/mcp/mcp-lms
COPY ../nanobot-websocket-channel/nanobot-webchat /app/nanobot-websocket-channel/nanobot-webchat
COPY ../nanobot-websocket-channel/mcp-webchat /app/nanobot-websocket-channel/mcp-webchat
COPY ../nanobot-websocket-channel/nanobot-channel-protocol /app/nanobot-websocket-channel/nanobot-channel-protocol

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e /app/mcp/mcp-lms

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e /app/nanobot-websocket-channel/nanobot-channel-protocol

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e /app/nanobot-websocket-channel/nanobot-webchat

RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --system -e /app/nanobot-websocket-channel/mcp-webchat

# ---
# Stage 2: final image
# ---

ARG REGISTRY_PREFIX_DOCKER_HUB
FROM ${REGISTRY_PREFIX_DOCKER_HUB}python:3.14.2-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV LANG=C.UTF-8

RUN apt-get update && apt-get install -y --no-install-recommends gosu && rm -rf /var/lib/apt/lists/*

# Setup a non-root user
RUN groupadd --system --gid 999 nonroot \
    && useradd --system --gid 999 --uid 999 --create-home nonroot

# Copy the application from the builder
COPY --from=builder --chown=nonroot:nonroot /app /app

# Set PATH to include venv
ENV PATH="/app/.venv/bin:$PATH"

WORKDIR /app/nanobot

HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8765/')" || exit 1

ENTRYPOINT ["python", "/app/nanobot/entrypoint.py"]
