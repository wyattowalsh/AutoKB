import pytest
from unittest.mock import patch, MagicMock
from my_agent.agent import graph
from my_agent.utils.state import AgentState

@pytest.fixture
def mock_state():
    return AgentState(messages=[], covered_topics=set(), topics_queue=[])

def test_description_agent(mock_state):
    with patch('my_agent.utils.nodes.call_model') as mock_call_model:
        mock_call_model.return_value = "Description generated"
        result = graph.run("description_agent", mock_state)
        assert result == "Description generated"
        mock_call_model.assert_called_once()

def test_knowledge_graph_agent(mock_state):
    with patch('my_agent.utils.nodes.call_model') as mock_call_model:
        mock_call_model.return_value = "Knowledge graph generated"
        result = graph.run("knowledge_graph_agent", mock_state)
        assert result == "Knowledge graph generated"
        mock_call_model.assert_called_once()

def test_related_topics_agent(mock_state):
    with patch('my_agent.utils.nodes.call_model') as mock_call_model:
        mock_call_model.return_value = "Related topics generated"
        result = graph.run("related_topics_agent", mock_state)
        assert result == "Related topics generated"
        mock_call_model.assert_called_once()

def test_action_agent(mock_state):
    with patch('my_agent.utils.nodes.tool_node') as mock_tool_node:
        mock_tool_node.return_value = "Action executed"
        result = graph.run("action", mock_state)
        assert result == "Action executed"
        mock_tool_node.assert_called_once()
