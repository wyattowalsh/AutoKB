from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.tools.serper import SerperSearchResults
from cachetools import TTLCache, cached

# Define the cache with a TTL of 24 hours (86400 seconds)
cache = TTLCache(maxsize=100, ttl=86400)

# Define the tools
tools = [
    TavilySearchResults(max_results=5),
    SerperSearchResults(max_results=5)
]

# Caching decorator for tool results
@cached(cache)
def get_tool_results(tool, query):
    return tool.run(query)
