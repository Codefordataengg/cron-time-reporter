import sys
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

import click
from loguru import logger

LOG_FILE = Path("logs/time.log")


def _configure_logger() -> None:
    logger.remove()
    logger.add(
        LOG_FILE,
        format="{time:YYYY-MM-DD HH:mm:ss} {extra[timezone]} | {message}",
        rotation="1 MB",
        retention=5,
        encoding="utf-8",
    )


def _get_timezone() -> str:
    try:
        # Works on Linux/macOS; falls back gracefully on Windows
        tz_path = Path("/etc/timezone")
        if tz_path.exists():
            return tz_path.read_text().strip()
        import time as _time
        return _time.tzname[0]
    except Exception:
        return "UTC"


@click.command()
@click.option(
    "--report",
    "n",
    type=click.IntRange(min=1),
    default=None,
    metavar="N",
    help="Print the last N log entries instead of logging.",
)
def cli(n: int | None) -> None:
    """Log current datetime and timezone, or report recent entries."""
    if n is not None:
        if not LOG_FILE.exists():
            click.echo("No log file found yet. Run without --report first to create one.")
            sys.exit(0)
        lines = LOG_FILE.read_text(encoding="utf-8").splitlines()
        for line in lines[-n:]:
            click.echo(line)
        return

    tz_name = _get_timezone()
    try:
        now = datetime.now(ZoneInfo(tz_name))
    except (ZoneInfoNotFoundError, Exception):
        now = datetime.now(ZoneInfo("UTC"))
        tz_name = "UTC"

    _configure_logger()
    logger.bind(timezone=tz_name).info(f"{now.strftime('%Y-%m-%d %H:%M:%S %Z%z')}")
    click.echo(f"Logged: {now.strftime('%Y-%m-%d %H:%M:%S')} ({tz_name})")


if __name__ == "__main__":
    cli()
