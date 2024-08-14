# Enhanced node functions for better model handling, error checking, and integration with the CLI
import logging
import os
from functools import lru_cache

import matplotlib.pyplot as plt
import networkx as nx
import requests
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langfuse.decorators import langfuse_context, observe
from langgraph.prebuilt import ToolNode
from rich.logging import RichHandler

from autokb.utils.tools import get_tool_results, tools

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[RichHandler()]
)
logger = logging.getLogger(__name__)

@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(
            temperature=0,
            model_name="gpt-4o",
            openai_api_key=os.getenv("OPENAI_API_KEY")  # Load from .env
        )
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not based on feedback
def should_continue_based_on_feedback(state):
    last_message = state["messages"][-1]
    if "retry" in last_message["content"]:
        return "retry"
    elif "continue" in last_message["content"]:
        return "continue"
    else:
        return "end"

# Define the function that calls the model
@observe(langfuse_instance)
def call_model(state, config, prompt):
    state["messages"].append({"role": "user", "content": prompt})
    logger.info(f"Calling model with prompt: {prompt}")
    return _get_model(config['agent']['model']).run(state)

# Define functions for generating content
@observe(langfuse_instance)
def generate_description(state, config):
    description_prompt = f"""
    Generate a detailed description of the topic around {config['agent']['description_max_words']} words.
    Ensure to use advanced Markdown formatting like **bold**, *italic*, [links](url), footnotes[^1], and lists.
    """
    return call_model(state, config, description_prompt)

@observe(langfuse_instance)
def generate_knowledge_graph(state, config):
    knowledge_graph_prompt = """
    Create a knowledge graph using entity relation semantic triplets and advanced, styled mermaid.js markdown syntax.
    """
    return call_model(state, config, knowledge_graph_prompt)

@observe(langfuse_instance)
def generate_related_topics(state, config):
    related_topics_prompt = """
    Generate a list of related topics (up to 25) using bulleted list and wikilinks link notation.
    """
    return call_model(state, config, related_topics_prompt)

@observe(langfuse_instance)
def generate_core_concepts(state, config):
    core_concepts_prompt = """
    Provide a detailed overview of core concepts related to the topic, including definitions, relevance, and principles.
    """
    return call_model(state, config, core_concepts_prompt)

@observe(langfuse_instance)
def generate_applications(state, config):
    applications_prompt = """
    Describe real-world applications of the topic, including examples, case studies, and industry use cases.
    """
    return call_model(state, config, applications_prompt)

@observe(langfuse_instance)
def generate_resources_tools(state, config):
    resources_tools_prompt = """
    List essential resources and tools related to the topic, explaining their relevance and value.
    """
    result = call_model(state, config, resources_tools_prompt)

    # Verify URLs in the result
    verified_resources = []
    for resource in result:
        if verify_url(resource['url']):
            verified_resources.append(resource)
        else:
            logger.warning(f"URL not live: {resource['url']}")

    return verified_resources

@observe(langfuse_instance)
def generate_research_questions(state, config):
    research_questions_prompt = """
    Identify recent developments and open research questions in the field.
    """
    return call_model(state, config, research_questions_prompt)

@observe(langfuse_instance)
def generate_historical_context(state, config):
    historical_context_prompt = """
    Provide a historical overview of the topic using mermaid.js timeline syntax, including key milestones and figures.
    Use advanced styling to differentiate between milestones and key figures, ensuring the timeline is visually engaging.
    """
    return call_model(state, config, historical_context_prompt)

@observe(langfuse_instance)
def generate_ethical_considerations(state, config):
    ethical_considerations_prompt = """
    Discuss ethical considerations related to the topic, providing balanced perspectives and frameworks.
    """
    return call_model(state, config, ethical_considerations_prompt)

@observe(langfuse_instance)
def generate_future_directions(state, config):
    future_directions_prompt = """
    Speculate on future trends and directions in the topic, offering foresight into opportunities and challenges.
    """
    return call_model(state, config, future_directions_prompt)

# Summarize search results from multiple tools
@observe(langfuse_instance)
def summarize_search_results(state, config):
    query = state["query"]
    search_summaries = []
    
    # Iterate through all tools to gather search results
    for tool_name, tool in tools.items():
        result = get_tool_results(tool, query, state["topic"])
        search_summaries.append(f"Results from {tool_name}: {result}")
    
    # Combine summaries into a single message
    summary = "\n".join(search_summaries)
    state["messages"].append({"role": "user", "content": summary})
    
    logger.info(f"Search summary generated: {summary}")
    return summary

# Define a feedback loop that refines content based on user input
def refine_based_on_feedback(state, config, refinement_prompt):
    feedback_prompt = f"""
    Based on the feedback received, refine the content to improve clarity, accuracy, and relevance.
    {refinement_prompt}
    """
    logger.info(f"Refining content with prompt: {feedback_prompt}")
    return call_model(state, config, feedback_prompt)

# Integrate the refinement process into the main workflow
def iterative_refinement(state, config):
    while should_continue_based_on_feedback(state) == "retry":
        refinement_prompt = state["messages"][-1]["content"]
        result = refine_based_on_feedback(state, config, refinement_prompt)
        state["messages"].append({"role": "assistant", "content": result})
        logger.info(f"Refinement result: {result}")
    return state["messages"][-1]["content"]

# Function to dynamically update agent configuration
def update_agent_config(state, new_config):
    config.update(new_config)
    logger.info(f"Agent configuration updated: {new_config}")
    return config

# Utility to save the LangGraph system diagram as PNG using NetworkX
def save_langgraph_as_png(graph, file_name="langgraph_system.png"):
    """
    Convert the LangGraph workflow into a NetworkX graph and save it as a PNG file.

    :param graph: The compiled LangGraph system (workflow).
    :param file_name: The name of the output PNG file.
    """
    G = nx.DiGraph()

    # Traverse the LangGraph workflow to add nodes and edges to the NetworkX graph
    for node in graph.nodes():
        G.add_node(node)

    for source, target, data in graph.edges(data=True):
        G.add_edge(source, target, label=data.get('label', ''))

    # Set the layout for the graph
    pos = nx.spring_layout(G, seed=42)  # positions for all nodes

    plt.figure(figsize=(12, 12))
    
    # Draw nodes and edges
    nx.draw(G, pos, with_labels=True, node_color='skyblue', node_size=3000, edge_color='gray', font_size=10, font_weight='bold')
    
    # Draw edge labels
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_color='red')

    # Save the graph as a PNG file
    plt.savefig(file_name, format="PNG")
    plt.close()

# Function to verify if a URL is live
def verify_url(url):
    try:
        response = requests.head(url, allow_redirects=True, timeout=5)
        return response.status_code == 200
    except requests.RequestException:
        return False

