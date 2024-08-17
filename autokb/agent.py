from langchain import LangChain
from llama_index import LlamaIndex
from langfuse import LangFuse
from langsmith import LangSmith
from loguru import logger
from rich import print
from tenacity import retry, stop_after_attempt, wait_fixed

class ResearcherAgent:
    def __init__(self, search_tool):
        self.search_tool = search_tool

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def conduct_research(self, topic):
        logger.info(f"Conducting research on topic: {topic}")
        results = self.search_tool.search(topic)
        return self.synthesize_results(results)

    def synthesize_results(self, results):
        # Synthesize, distill, and summarize the search results
        synthesized_results = "Synthesized results"
        return synthesized_results

    def generate_search_query(self, topic):
        # Generate intelligent, well-crafted, robust search query
        search_query = f"Search query for {topic}"
        return search_query


class PageDataGeneratorAgent:
    def __init__(self):
        pass

    def generate_page_data(self, topic, research_data):
        logger.info(f"Generating page data for topic: {topic}")
        llm = LangChain()
        page_data = llm.generate_page_data(research_data, mode="JSON")
        return page_data

    def extract_tags(self, research_data):
        # Use LLM to generate tags from research data
        llm = LangChain()
        tags = llm.generate_tags(research_data)
        return tags

    def extract_aliases(self, research_data):
        # Use LLM to generate aliases from research data
        llm = LangChain()
        aliases = llm.generate_aliases(research_data)
        return aliases

    def get_current_datetime(self):
        # Get the current datetime in the specified format
        from datetime import datetime
        return datetime.now().isoformat()

    def generate_description(self, research_data):
        # Generate a comprehensive description for the topic
        return "Comprehensive description"

    def generate_knowledge_graph(self, research_data):
        # Generate a knowledge graph in mermaid.js markdown format
        return "Knowledge graph"

    def generate_related_topics(self, research_data):
        # Generate a list of related topics
        return ["Related Topic 1", "Related Topic 2"]

    def generate_resources(self, research_data):
        # Generate a list of related resources
        return ["Resource 1", "Resource 2"]

    def generate_kb_page(self, topic, research_data):
        # Generate knowledge base page following the template specified in the README.md
        kb_page = f"""
        ---
        title: {topic.title()}
        tags: {self.extract_tags(research_data)}
        aliases: {self.extract_aliases(research_data)}
        created: {self.get_current_datetime()}
        updated: {self.get_current_datetime()}
        ---

        # {topic.title()}

        {self.generate_description(research_data)}

        {self.generate_knowledge_graph(research_data)}

        ---

        ## Related Topics

        {self.generate_related_topics(research_data)}

        ---

        ## Resources

        {self.generate_resources(research_data)}
        """
        return kb_page


class ManagerResearcherAgent:
    def __init__(self, researchers):
        self.researchers = researchers

    def manage_research(self, topic):
        logger.info(f"Managing research for topic: {topic}")
        all_results = []
        for researcher in self.researchers:
            result = researcher.conduct_research(topic)
            all_results.append(result)
        return self.compile_results(all_results)

    def compile_results(self, all_results):
        # Compile the results from all researchers
        compiled_results = "Compiled results"
        return compiled_results

    def compile_output_for_data_generator(self, all_results):
        # Compile output for input to the data generator
        compiled_output = "Compiled output for data generator"
        return compiled_output
