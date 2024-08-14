from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
from tqdm import tqdm
import sys
import os

# Initialize Rich console
console = Console()

def setup_logging(config):
    log_level = config.get("logging", {}).get("level", "INFO")
    log_format = config.get("logging", {}).get("format", "{time} - {name} - {level} - {message}")
    log_to_file = config.get("logging", {}).get("log_to_file", True)
    log_file_path = config.get("logging", {}).get("log_file_path", "./logs/agent.log")
    verbosity = config.get("logging", {}).get("verbosity", 1)

    # Remove default logger
    logger.remove()

    # Add RichHandler for console logging
    if verbosity > 0:
        logger.add(RichHandler(console=console, level=log_level, format=log_format))

    # Add file handler for logging to file
    if log_to_file:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logger.add(log_file_path, level=log_level, format=log_format, rotation="10 MB")

    # Add structured rotating file handler
    logger.add("logs/structured_{time}.log", level=log_level, format=log_format, rotation="10 MB", serialize=True)

    # Add tqdm handler for progress bars
    logger.add(lambda msg: tqdm.write(msg, end=''), level=log_level, format=log_format)

    return logger
