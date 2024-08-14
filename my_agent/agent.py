from typing import TypedDict, Literal

from langgraph.graph import StateGraph, END
from my_agent.utils.nodes import call_model, should_continue, tool_node, generate_description, generate_knowledge_graph, generate_related_topics
from my_agent.utils.state import AgentState

# Define the config
class GraphConfig(TypedDict):
    model_name: Literal["openai"]
    max_depth: int

# Define a new graph
workflow = StateGraph(AgentState, config_schema=GraphConfig)

# Define the nodes for different agents
workflow.add_node("description_agent", generate_description)
workflow.add_node("knowledge_graph_agent", generate_knowledge_graph)
workflow.add_node("related_topics_agent", generate_related_topics)
workflow.add_node("action", tool_node)

# Set the entrypoint as `description_agent`
workflow.set_entry_point("description_agent")

# Add conditional edges for iterative generation
workflow.add_conditional_edges(
    "description_agent",
    should_continue,
    {
        "continue": "knowledge_graph_agent",
        "end": END,
    },
)

workflow.add_conditional_edges(
    "knowledge_graph_agent",
    should_continue,
    {
        "continue": "related_topics_agent",
        "end": END,
    },
)

workflow.add_conditional_edges(
    "related_topics_agent",
    should_continue,
    {
        "continue": "action",
        "end": END,
    },
)

# Add normal edges for cycling through agents
workflow.add_edge("action", "description_agent")

# Finally, we compile it!
graph = workflow.compile()
from my_agent.utils.state import AgentState


# Define the config
    model_name: Literal["openai"]


# Define a new graph
workflow.add_node("generate_related_topics", generate_related_topics)

# Set the entrypoint as `generate_description`
workflow.set_entry_point("generate_description")

# Add conditional edges for iterative generation
    should_continue,
    {
        "continue": "generate_knowledge_graph",
    },
)

workflow.add_conditional_edges(
    "generate_knowledge_graph",
    should_continue,
    {
    },
)

# This compiles it into a LangChain Runnable,
# meaning you can use it as you would any other runnable
graph = workflow.compile()
