FROM python:3.12-slim-bookworm AS python_base

FROM python_base AS development

ENV STAGE=development

RUN <<EOF
    apt-get update && apt-get install -y --no-install-recommends \
        git
    rm -rf /var/lib/apt/lists/*
EOF

ARG USER_NAME=backend
ARG GROUP_NAME=backend
ARG UID=${UID:-1000}
ARG GID=${UID:-1000}

RUN <<EOF
    groupadd --gid ${GID} ${GROUP_NAME}
    useradd --uid ${UID} --gid ${GID} --shell /bin/bash --create-home ${USER_NAME}
EOF

COPY --from=ghcr.io/astral-sh/uv:0.5.9  --chown={UID}:{GID} /uv /uvx /bin/
COPY --chown=${USER_NAME}:${GROUP_NAME} ./ /src/backend

WORKDIR /src/backend

RUN uv sync --frozen --no-cache

USER ${USER_NAME}

CMD uv run uvicorn main:app --host 0.0.0.0 --port 8000 --reload
