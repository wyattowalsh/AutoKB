import pytest
from unittest.mock import patch, MagicMock
from autokb.utils.nodes import call_model, should_continue, generate_description, generate_knowledge_graph, generate_related_topics

@pytest.fixture
def mock_state():
    return {
        "messages": [],
        "covered_topics": set(),
        "topics_queue": []
    }

def test_call_model(mock_state):
    with patch('my_agent.utils.nodes._get_model') as mock_get_model:
        mock_model = MagicMock()
        mock_get_model.return_value = mock_model
        mock_model.return_value = "Model called"
        result = call_model(mock_state, {"agent": {"description_max_words": 1000}})
        assert result == "Model called"
        mock_get_model.assert_called_once()

def test_should_continue():
    state = {"messages": [{"tool_calls": []}]}
    result = should_continue(state)
    assert result == "end"
    state = {"messages": [{"tool_calls": ["call"]}]}
    result = should_continue(state)
    assert result == "continue"

def test_generate_description(mock_state):
    with patch('my_agent.utils.nodes.call_model') as mock_call_model:
        mock_call_model.return_value = "Description generated"
        result = generate_description(mock_state, {"agent": {"description_max_words": 1000}})
        assert result == "Description generated"
        mock_call_model.assert_called_once()

def test_generate_knowledge_graph(mock_state):
    with patch('my_agent.utils.nodes.call_model') as mock_call_model:
        mock_call_model.return_value = "Knowledge graph generated"
        result = generate_knowledge_graph(mock_state, {})
        assert result == "Knowledge graph generated"
        mock_call_model.assert_called_once()

def test_generate_related_topics(mock_state):
    with patch('my_agent.utils.nodes.call_model') as mock_call_model:
        mock_call_model.return_value = "Related topics generated"
        result = generate_related_topics(mock_state, {})
        assert result == "Related topics generated"
        mock_call_model.assert_called_once()
