import pytest
from pathlib import Path
from dataops.utils.logger import setup_logger

def test_logger_creates_file(tmp_path, monkeypatch):
    # Monkeypatch Path("logs") to use tmp_path so we don't pollute current dir
    monkeypatch.chdir(tmp_path)
    
    logger = setup_logger("test_logger")
    logger.info("Test log message")
    
    log_file = tmp_path / "logs" / "dataops.log"
    assert log_file.exists()
    
    with open(log_file, "r") as f:
        content = f.read()
        assert "Test log message" in content
