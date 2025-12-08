import logging
import sys
import os
from pathlib import Path

def setup_logger(name="dataops", level=logging.INFO):
    """
    Sets up a professional logger with stdout and file handlers.
    Logs are saved to a 'logs' directory in the current working directory.
    
    Args:
        name (str): Name of the logger.
        level (int): Logging level (default: logging.INFO).
        
    Returns:
        logging.Logger: Configured logger instance.
    """
    logger = logging.getLogger(name)
    logger.setLevel(level)

    if not logger.handlers:
        # Formatter
        formatter = logging.Formatter(
            "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        # Stream Handler (Console)
        stream_handler = logging.StreamHandler(sys.stdout)
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)
        logger.addHandler(stream_handler)

        # File Handler
        log_dir = Path("logs")
        log_dir.mkdir(exist_ok=True)
        
        file_handler = logging.FileHandler(log_dir / "dataops.log", encoding='utf-8')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger
