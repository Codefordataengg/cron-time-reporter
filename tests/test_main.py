import re
from pathlib import Path

import pytest
from click.testing import CliRunner
from loguru import logger

from src.main import cli


@pytest.fixture(autouse=True)
def isolated_log(tmp_path, monkeypatch):
    """Redirect LOG_FILE to a temp directory and reset loguru between tests."""
    import src.main as main_module
    log_file = tmp_path / "time.log"
    monkeypatch.setattr(main_module, "LOG_FILE", log_file)
    yield log_file
    logger.remove()


def test_logging_creates_log_file(isolated_log):
    runner = CliRunner()
    result = runner.invoke(cli, [])
    assert result.exit_code == 0
    assert isolated_log.exists()


def test_log_file_contains_timestamp_entry(isolated_log):
    runner = CliRunner()
    runner.invoke(cli, [])
    content = isolated_log.read_text(encoding="utf-8")
    # Expect a line matching: YYYY-MM-DD HH:MM:SS <timezone> | <datetime string>
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}", content)


def test_report_returns_correct_number_of_lines(isolated_log):
    runner = CliRunner()
    # Write 5 log entries
    for _ in range(5):
        runner.invoke(cli, [])
    result = runner.invoke(cli, ["--report", "3"])
    assert result.exit_code == 0
    lines = [l for l in result.output.splitlines() if l.strip()]
    assert len(lines) == 3


def test_report_with_more_lines_than_exist(isolated_log):
    runner = CliRunner()
    runner.invoke(cli, [])
    result = runner.invoke(cli, ["--report", "100"])
    assert result.exit_code == 0
    # Should return however many lines exist, not crash
    lines = [l for l in result.output.splitlines() if l.strip()]
    assert len(lines) >= 1


def test_report_graceful_message_when_log_missing(isolated_log):
    runner = CliRunner()
    # Do not invoke cli first — log file does not exist
    result = runner.invoke(cli, ["--report", "5"])
    assert result.exit_code == 0
    assert "No log file found" in result.output
