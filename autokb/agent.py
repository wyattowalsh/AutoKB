from typing import TypedDict, Literal
from langgraph.graph import StateGraph, END
from autokb.utils.nodes import (
    call_model,
    should_continue_based_on_feedback,
    generate_description,
    generate_knowledge_graph,
    generate_related_topics,
    generate_core_concepts,
    generate_applications,
    generate_resources_tools,
    generate_research_questions,
    generate_historical_context,
    generate_ethical_considerations,
    generate_future_directions,
    tool_node,
    summarize_search_results,
    oracle_decision_node,
    save_langgraph_as_png
)
from autokb.utils.state import AgentState

class GraphConfig(TypedDict):
    model_name: Literal["openai"]
    max_depth: int

workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Oracle node for decision making
workflow.add_node("oracle_node", oracle_decision_node)

# Adding agents for each search tool
workflow.add_node("serper_agent", tool_node)
workflow.add_node("tavily_agent", tool_node)
workflow.add_node("reddit_agent", tool_node)
workflow.add_node("searxng_agent", tool_node)
workflow.add_node("semantic_scholar_agent", tool_node)
workflow.add_node("wikidata_agent", tool_node)
workflow.add_node("wikipedia_agent", tool_node)

# Add the GitHub API tool as an agent node
workflow.add_node("github_agent", tool_node)

# Summarize results from all search agents
workflow.add_node("search_summarizer", summarize_search_results)

# Nodes for generating knowledge base content
workflow.add_node("description_agent", generate_description)
workflow.add_node("knowledge_graph_agent", generate_knowledge_graph)
workflow.add_node("related_topics_agent", generate_related_topics)
workflow.add_node("core_concepts_agent", generate_core_concepts)
workflow.add_node("applications_agent", generate_applications)
workflow.add_node("resources_tools_agent", generate_resources_tools)
workflow.add_node("research_questions_agent", generate_research_questions)
workflow.add_node("historical_context_agent", generate_historical_context)
workflow.add_node("ethical_considerations_agent", generate_ethical_considerations)
workflow.add_node("future_directions_agent", generate_future_directions)

# Set the entry point as the Oracle node
workflow.set_entry_point("oracle_node")

# Implement advanced cyclic feedback loop
workflow.add_conditional_edges(
    "oracle_node",
    should_continue_based_on_feedback,
    {
        "retry": "oracle_node",
        "continue": "description_agent",
        "end": END,
    },
)

workflow.add_conditional_edges(
    "description_agent",
    should_continue_based_on_feedback,
    {
        "retry": "description_agent",
        "continue": "knowledge_graph_agent",
        "end": END,
    },
)

workflow.add_conditional_edges(
    "knowledge_graph_agent",
    should_continue_based_on_feedback,
    {
        "retry": "knowledge_graph_agent",
        "continue": "related_topics_agent",
        "end": END,
    },
)

# Cyclic flow for iterative refinement and error checking
workflow.add_edge("related_topics_agent", "core_concepts_agent")
workflow.add_edge("core_concepts_agent", "applications_agent")
workflow.add_edge("applications_agent", "resources_tools_agent")
workflow.add_edge("resources_tools_agent", "research_questions_agent")
workflow.add_edge("research_questions_agent", "historical_context_agent")
workflow.add_edge("historical_context_agent", "ethical_considerations_agent")
workflow.add_edge("ethical_considerations_agent", "future_directions_agent")
workflow.add_edge("future_directions_agent", "oracle_node")  # Cyclic flow back to the Oracle

# Compile the graph with enhanced features
graph = workflow.compile()

# Save the LangGraph system diagram as PNG for visualization in LangGraph Studio
save_langgraph_as_png(graph, file_name="langgraph_system.png")
