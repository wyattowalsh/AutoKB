from langchain_community.utilities import GoogleSerperAPIWrapper
from langchain_community.tools.tavily_search import TavilySearchResults
from cachetools import TTLCache, cached

# Define the cache with a TTL of 24 hours (86400 seconds)
cache = TTLCache(maxsize=100, ttl=86400)

# Define the tools
tools = {
    "tavily": TavilySearchResults(max_results=5),
    "serper": GoogleSerperAPIWrapper(max_results=5)
}

# Caching decorator for tool results
@cached(cache)
def get_tool_results(tool, query):
    return tool.run(query)

# Function to get results based on config
def get_results(query, config):
    tool_choice = config.get("tools", {}).get("tool_choice", "both")
    results = []
    if tool_choice in ["tavily", "both"]:
        results.append(get_tool_results(tools["tavily"], query))
    if tool_choice in ["serper", "both"]:
        results.append(get_tool_results(tools["serper"], query))
    return results
