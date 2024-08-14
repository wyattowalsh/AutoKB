import pytest
from unittest.mock import patch, MagicMock
from my_agent.utils.generate_kb import generate_kb_page, generate_knowledge_graph_triplets
from my_agent.utils.schema import Description, KnowledgeGraph, RelatedTopics, SemanticTriple

@pytest.fixture
def mock_description():
    return Description(topic="Test Topic", content="This is a test description.")

@pytest.fixture
def mock_knowledge_graph():
    return KnowledgeGraph(topic="Test Topic", graph=[
        SemanticTriple(source="Entity1", target="Entity2", relation="related to"),
        SemanticTriple(source="Entity2", target="Entity3", relation="part of")
    ])

@pytest.fixture
def mock_related_topics():
    return RelatedTopics(topic="Test Topic", related_topics=["Related Topic 1", "Related Topic 2"])

def test_generate_kb_page(mock_description, mock_knowledge_graph, mock_related_topics, tmp_path):
    output_dir = tmp_path / "kb_output"
    output_dir.mkdir()
    generate_kb_page(mock_description, mock_knowledge_graph, mock_related_topics, str(output_dir))
    generated_file = output_dir / "Test Topic.md"
    assert generated_file.exists()
    with open(generated_file, 'r') as file:
        content = file.read()
        assert "# Test Topic" in content
        assert "This is a test description." in content
        assert "```mermaid" in content
        assert "Entity1 -->|related to| Entity2" in content
        assert "Entity2 -->|part of| Entity3" in content
        assert "## Related Topics" in content
        assert "- [[Related Topic 1]]" in content
        assert "- [[Related Topic 2]]" in content

def test_generate_knowledge_graph_triplets(mock_knowledge_graph):
    triplets = mock_knowledge_graph.graph
    result = generate_knowledge_graph_triplets(triplets)
    assert "```mermaid" in result
    assert "Entity1 -->|related to| Entity2" in result
    assert "Entity2 -->|part of| Entity3" in result
