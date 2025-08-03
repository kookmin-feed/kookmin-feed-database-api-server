FROM ghcr.io/astral-sh/uv:debian-slim

RUN apt-get update && \
    apt-get install -y \
    supervisor \
    curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
WORKDIR /app
COPY . .

RUN uv sync --frozen

CMD ["supervisord", "-c", "supervisord.conf"]