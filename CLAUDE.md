# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What It Does

Logs the current datetime and timezone to a rotating log file each time it runs. Supports a `--report N` flag to print the last N log entries. Intended to be run on a schedule (e.g. via cron or Docker).

## Tech Stack

- **Python 3.11**, **uv** for package management
- **loguru** for logging, **click** for CLI
- **Docker** / **docker-compose** for local running
- **GitHub Actions** for CI/CD, **GHCR** for image registry

## Common Commands

```bash
# Install dependencies
uv sync

# Run the scheduler (log current datetime)
uv run python -m src.main

# Print last N log entries
uv run python -m src.main --report 20

# Run tests
uv run pytest

# Run a single test file
uv run pytest tests/test_main.py

# Build Docker image
docker build -t cron-time-reporter .

# Run with docker-compose
docker-compose up
```

## Project Structure

- `src/` — application source code
- `tests/` — test suite
- `logs/` — rotating log file output
- `.devcontainer/` — VS Code dev container configuration