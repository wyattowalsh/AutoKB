import typer
from autokb.agent import ResearcherAgent, PageDataGeneratorAgent, ManagerResearcherAgent

app = typer.Typer()

@app.command()
def generate_new_kb(seed_topics: list[str]):
    researchers = [ResearcherAgent(search_tool) for search_tool in ["Tavily Search", "Serper", "Arxiv", "Wikipedia", "Wikidata", "Reddit Search", "Exa Search", "StackExchange"]]
    manager = ManagerResearcherAgent(researchers)
    page_data_generator = PageDataGeneratorAgent()

    for topic in seed_topics:
        research_data = manager.manage_research(topic)
        page_data = page_data_generator.generate_page_data(topic, research_data)
        print(page_data)

@app.command()
def continue_existing_kb(seed_topics: list[str]):
    researchers = [ResearcherAgent(search_tool) for search_tool in ["Tavily Search", "Serper", "Arxiv", "Wikipedia", "Wikidata", "Reddit Search", "Exa Search", "StackExchange"]]
    manager = ManagerResearcherAgent(researchers)
    page_data_generator = PageDataGeneratorAgent()

    for topic in seed_topics:
        research_data = manager.manage_research(topic)
        page_data = page_data_generator.generate_page_data(topic, research_data)
        print(page_data)

if __name__ == "__main__":
    app()
