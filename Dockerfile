FROM ghcr.io/astral-sh/uv:python3.10-alpine
EXPOSE 8000
WORKDIR /app
COPY . .

RUN apk add --no-cache curl
RUN uv sync --frozen

CMD ["uv", "run", "python", "main.py"]