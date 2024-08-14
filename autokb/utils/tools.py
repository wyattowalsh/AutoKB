import os
from langchain_community.utilities import (
    GoogleSerperAPIWrapper,
    SemanticScholarAPIWrapper,
    WikidataAPIWrapper,
    WikipediaAPIWrapper
)
from langchain_community.utilities.reddit_search import RedditSearchAPIWrapper
from langchain_community.utilities.searx_search import SearxSearchWrapper
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper

# Initialize SQLite database
from autokb.utils.sqlite_db import (
    get_tool_responses,
    initialize_db,
    save_tool_response
)

initialize_db()

# Define the tools conditionally based on config settings
tools = {}

if os.getenv("SERPER_ENABLED", "true").lower() == "true":
    tools["serper"] = GoogleSerperAPIWrapper(api_key=os.getenv("SERPER_API_KEY"))

if os.getenv("TAVILY_ENABLED", "true").lower() == "true":
    tools["tavily"] = TavilySearchAPIWrapper(api_key=os.getenv("TAVILY_API_KEY"))

if os.getenv("REDDIT_ENABLED", "true").lower() == "true":
    tools["reddit"] = RedditSearchAPIWrapper(
        reddit_client_id=os.getenv("REDDIT_CLIENT_ID"),
        reddit_client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
        reddit_user_agent=os.getenv("REDDIT_USER_AGENT")
    )

if os.getenv("SEARXNG_ENABLED", "true").lower() == "true":
    tools["searxng"] = SearxSearchWrapper(api_base=os.getenv("SEARXNG_API_BASE"))

if os.getenv("SEMANTIC_SCHOLAR_ENABLED", "true").lower() == "true":
    tools["semantic_scholar"] = SemanticScholarAPIWrapper(api_key=os.getenv("SEMANTIC_SCHOLAR_API_KEY"))

if os.getenv("WIKIDATA_ENABLED", "true").lower() == "true":
    tools["wikidata"] = WikidataAPIWrapper()

if os.getenv("WIKIPEDIA_ENABLED", "true").lower() == "true":
    tools["wikipedia"] = WikipediaAPIWrapper()

def get_tool_results(tool, query, topic):
    """
    Run the tool with the given query and persist the results in SQLite.
    """
    result = tool.run(query)
    save_tool_response(topic, query, tool.__class__.__name__, result)
    return result

def get_persisted_tool_responses(topic, tool_name=None):
    """
    Retrieve persisted tool responses for a given topic, optionally filtered by tool name.
    """
    return get_tool_responses(topic, tool_name)

# Optionally, adding a function to perform parallel execution of tool queries
def run_all_tools_in_parallel(query, topic):
    """
    Run all enabled tools in parallel and persist the results.
    """
    from concurrent.futures import ThreadPoolExecutor
    
    with ThreadPoolExecutor() as executor:
        futures = [
            executor.submit(get_tool_results, tool, query, topic)
            for tool_name, tool in tools.items()
        ]
        results = [future.result() for future in futures]

    return results
