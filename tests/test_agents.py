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

def test_page_data_generator_agent_generate_page_data(page_data_generator_agent, mocker):
    topic = "Test Topic"
    research_data = "Research Data"
    
    mocker.patch.object(PageDataGeneratorAgent, 'extract_tags', return_value=['tag1', 'tag2'])
    mocker.patch.object(PageDataGeneratorAgent, 'extract_aliases', return_value=['alias1', 'alias2'])
    
    page_data = page_data_generator_agent.generate_page_data(topic, research_data)
    assert page_data["title"] == "Test Topic"
    assert page_data["tags"] == ['tag1', 'tag2']
    assert page_data["aliases"] == ['alias1', 'alias2']
    assert "created" in page_data
    assert "updated" in page_data
    assert "description" in page_data
    assert "knowledge_graph" in page_data
    assert "related_topics" in page_data
    assert "resources" in page_data

def test_page_data_generator_agent_generate_kb_page(page_data_generator_agent, mocker):
    topic = "Test Topic"
    research_data = "Research Data"
    
    mocker.patch.object(PageDataGeneratorAgent, 'extract_tags', return_value=['tag1', 'tag2'])
    mocker.patch.object(PageDataGeneratorAgent, 'extract_aliases', return_value=['alias1', 'alias2'])
    
    kb_page = page_data_generator_agent.generate_kb_page(topic, research_data)
    assert "title: Test Topic" in kb_page
    assert "tags: ['tag1', 'tag2']" in kb_page
    assert "aliases: ['alias1', 'alias2']" in kb_page
    assert "created:" in kb_page
    assert "updated:" in kb_page
    assert "# Test Topic" in kb_page
    assert "Comprehensive description" in kb_page
    assert "Knowledge graph" in kb_page
    assert "Related Topics" in kb_page
    assert "Related Topic 1" in kb_page
    assert "Related Topic 2" in kb_page
    assert "Resources" in kb_page
    assert "Resource 1" in kb_page
    assert "Resource 2" in kb_page

def test_manager_researcher_agent_manage_research(manager_researcher_agent):
    topic = "Test Topic"
    compiled_results = manager_researcher_agent.manage_research(topic)
    assert compiled_results == "Compiled results"

def test_manager_researcher_agent_compile_output_for_data_generator(manager_researcher_agent):
    all_results = ["Result 1", "Result 2"]
    compiled_output = manager_researcher_agent.compile_output_for_data_generator(all_results)
    assert compiled_output == "Compiled output for data generator"

def test_researcher_agent_generate_search_query(researcher_agent):
    topic = "Test Topic"
    search_query = researcher_agent.generate_search_query(topic)
    assert search_query == "Search query for Test Topic"

def test_page_data_generator_agent_extract_tags(page_data_generator_agent):
    research_data = "Research Data"
    tags = page_data_generator_agent.extract_tags(research_data)
    assert tags == ["tag1", "tag2"]

def test_page_data_generator_agent_extract_aliases(page_data_generator_agent):
    research_data = "Research Data"
    aliases = page_data_generator_agent.extract_aliases(research_data)
    assert aliases == ["alias1", "alias2"]

def test_page_data_generator_agent_get_current_datetime(page_data_generator_agent):
    current_datetime = page_data_generator_agent.get_current_datetime()
    assert current_datetime is not None

def test_page_data_generator_agent_generate_description(page_data_generator_agent):
    research_data = "Research Data"
    description = page_data_generator_agent.generate_description(research_data)
    assert description == "Comprehensive description"

def test_page_data_generator_agent_generate_knowledge_graph(page_data_generator_agent):
    research_data = "Research Data"
    knowledge_graph = page_data_generator_agent.generate_knowledge_graph(research_data)
    assert knowledge_graph == "Knowledge graph"

def test_page_data_generator_agent_generate_related_topics(page_data_generator_agent):
    research_data = "Research Data"
    related_topics = page_data_generator_agent.generate_related_topics(research_data)
    assert related_topics == ["Related Topic 1", "Related Topic 2"]

def test_page_data_generator_agent_generate_resources(page_data_generator_agent):
    research_data = "Research Data"
    resources = page_data_generator_agent.generate_resources(research_data)
    assert resources == ["Resource 1", "Resource 2"]
