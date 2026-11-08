FROM python:3.14-slim-trixie AS builder
COPY --from=docker.io/astral/uv:0.13.6 /uv /uvx /bin/

ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy
ENV UV_NO_DEV=1
ENV UV_PYTHON_DOWNLOADS=0

WORKDIR /app

COPY pyproject.toml uv.lock ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv sync --locked --no-install-project

COPY . .
RUN uv sync --locked --no-editable

FROM python:3.14-slim-trixie AS runtime

WORKDIR /app
COPY --from=builder /app/.venv /app/.venv

RUN : \
    && groupadd --system --gid 999 nonroot \
    && useradd --system  --gid 999 --uid 999 --create-home nonroot

ENV PATH="/app/.venv/bin:${PATH}"
ENV PYTHONUNBUFFERED=1

WORKDIR /app
USER nonroot
