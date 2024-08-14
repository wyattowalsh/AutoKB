import pytest
from unittest.mock import patch, MagicMock
from autokb.utils.autokb_logging import setup_logging
from loguru import logger

@pytest.fixture
def mock_config():
    return {
        "logging": {
            "level": "INFO",
            "format": "{time} - {name} - {level} - {message}",
            "log_to_file": False,
            "log_file_path": "./logs/agent.log",
            "verbosity": 1
        }
    }

def test_setup_logging(mock_config):
    with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
        mock_logger.add = MagicMock()
        setup_logging(mock_config)
        assert mock_logger.add.call_count == 4

def test_logging_to_console(mock_config):
    with patch('my_agent.utils.kbgen_logging.console') as mock_console:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_logger.add.assert_any_call(mock_console, level="INFO", format="{time} - {name} - {level} - {message}")

def test_logging_to_file(mock_config):
    mock_config["logging"]["log_to_file"] = True
    with patch('my_agent.utils.kbgen_logging.os.makedirs') as mock_makedirs:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_makedirs.assert_called_once_with('./logs', exist_ok=True)
            mock_logger.add.assert_any_call('./logs/agent.log', level="INFO", format="{time} - {name} - {level} - {message}", rotation="10 MB")

def test_structured_logging(mock_config):
    with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
        mock_logger.add = MagicMock()
        setup_logging(mock_config)
        mock_logger.add.assert_any_call("logs/structured_{time}.log", level="INFO", format="{time} - {name} - {level} - {message}", rotation="10 MB", serialize=True)

def test_tqdm_logging(mock_config):
    with patch('my_agent.utils.kbgen_logging.tqdm') as mock_tqdm:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_logger.add.assert_any_call(lambda msg: mock_tqdm.write(msg, end=''), level="INFO", format="{time} - {name} - {level} - {message}")

def test_langfuse_tracing(mock_config):
    with patch('my_agent.utils.kbgen_logging.langfuse') as mock_langfuse:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_langfuse.trace.assert_called_once_with(mock_logger)

def test_langsmith_tracing(mock_config):
    with patch('my_agent.utils.kbgen_logging.langsmith') as mock_langsmith:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_langsmith.trace.assert_called_once_with(mock_logger)

def test_langfuse_monitoring(mock_config):
    with patch('my_agent.utils.kbgen_logging.langfuse') as mock_langfuse:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_langfuse.monitor.assert_called_once_with(mock_logger)

def test_langsmith_monitoring(mock_config):
    with patch('my_agent.utils.kbgen_logging.langsmith') as mock_langsmith:
        with patch('my_agent.utils.kbgen_logging.logger') as mock_logger:
            mock_logger.add = MagicMock()
            setup_logging(mock_config)
            mock_langsmith.monitor.assert_called_once_with(mock_logger)
