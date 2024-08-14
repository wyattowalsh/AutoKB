import pytest
from unittest.mock import patch, MagicMock
from autokb.utils.tools import get_tool_results, get_results, clear_cache, remove_cache_entry

@pytest.fixture
def mock_config():
    return {
        "tools": {
            "tool_choice": "both"
        }
    }

def test_get_tool_results():
    with patch('my_agent.utils.tools.tools') as mock_tools:
        mock_tool = MagicMock()
        mock_tool.run.return_value = "Tool results"
        mock_tools.__getitem__.return_value = mock_tool
        result = get_tool_results(mock_tool, "query")
        assert result == "Tool results"
        mock_tool.run.assert_called_once_with("query")

def test_get_results(mock_config):
    with patch('my_agent.utils.tools.get_tool_results') as mock_get_tool_results:
        mock_get_tool_results.return_value = "Tool results"
        result = get_results("query", mock_config)
        assert result == ["Tool results", "Tool results"]
        assert mock_get_tool_results.call_count == 2

def test_clear_cache():
    with patch('my_agent.utils.tools.cache') as mock_cache:
        clear_cache()
        mock_cache.clear.assert_called_once()

def test_remove_cache_entry():
    with patch('my_agent.utils.tools.cache') as mock_cache:
        mock_cache.__contains__.return_value = True
        remove_cache_entry("key")
        mock_cache.__delitem__.assert_called_once_with("key")
