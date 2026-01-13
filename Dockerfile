FROM python:3.13-slim-trixie

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV TZ="UTC"
ENV DEBIAN_FRONTEND=noninteractive

WORKDIR /app

RUN apt update && \
    apt -y install -qq curl libffi-dev && \
    apt -y clean

RUN curl -Ls https://astral.sh/uv/install.sh | sh
ENV PATH="/root/.local/bin:$PATH"

COPY pyproject.toml README.md ./
COPY src ./src

RUN uv venv
RUN uv sync --no-dev

ENV PYTHONPATH=/app

COPY . .
COPY ./entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
