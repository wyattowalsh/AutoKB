import pytest
from autokb.agent import ResearcherAgent, PageDataGeneratorAgent, ManagerResearcherAgent

class MockSearchTool:
    def search(self, topic):
        return [f"Result for {topic}"]

@pytest.fixture
def researcher_agent():
    return ResearcherAgent(search_tool=MockSearchTool())

@pytest.fixture
def page_data_generator_agent():
    return PageDataGeneratorAgent()

@pytest.fixture
def manager_researcher_agent(researcher_agent):
    return ManagerResearcherAgent(researchers=[researcher_agent])

def test_researcher_agent_conduct_research(researcher_agent):
    topic = "Test Topic"
    results = researcher_agent.conduct_research(topic)
    assert results == "Synthesized results"

def test_page_data_generator_agent_generate_page_data(page_data_generator_agent):
    topic = "Test Topic"
    research_data = "Research Data"
    page_data = page_data_generator_agent.generate_page_data(topic, research_data)
    assert page_data["title"] == "Test Topic"
    assert "tags" in page_data
    assert "aliases" in page_data
    assert "created" in page_data
    assert "updated" in page_data
    assert "description" in page_data
    assert "knowledge_graph" in page_data
    assert "related_topics" in page_data
    assert "resources" in page_data

def test_manager_researcher_agent_manage_research(manager_researcher_agent):
    topic = "Test Topic"
    compiled_results = manager_researcher_agent.manage_research(topic)
    assert compiled_results == "Compiled results"
