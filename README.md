# cron-time-reporter

<!-- TODO: short description -->

## Usage

```bash
# Log current datetime
uv run python -m src.main

# Print last N log entries
uv run python -m src.main --report 20
```

## Development

```bash
uv sync
uv run pytest
```

## Docker

```bash
docker-compose up
```
