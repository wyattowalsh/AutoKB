from functools import lru_cache
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


system_prompt = """Be a helpful assistant"""

# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "openai")
    model = _get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the function to execute tools
tool_node = ToolNode(tools)

# Define the function for generating descriptions
def generate_description(state, config):
    description_prompt = f"Generate a detailed description of the topic around {config['agent']['description_max_words']} words."
    state["messages"].append({"role": "user", "content": description_prompt})
    return call_model(state, config)

# Define the function for generating knowledge graphs
def generate_knowledge_graph(state, config):
    knowledge_graph_prompt = "Generate a knowledge graph for the topic using advanced, styled mermaid.js markdown syntax."
    state["messages"].append({"role": "user", "content": knowledge_graph_prompt})
    return call_model(state, config)

# Define the function for generating related topics
def generate_related_topics(state, config):
    related_topics_prompt = "Generate a list of related topics using bulleted list and wikilinks link notation."
    state["messages"].append({"role": "user", "content": related_topics_prompt})
    return call_model(state, config)
from functools import lru_cache
from langchain_openai import ChatOpenAI
from my_agent.utils.tools import tools
from langgraph.prebuilt import ToolNode


@lru_cache(maxsize=4)
def _get_model(model_name: str):
    if model_name == "openai":
        model = ChatOpenAI(temperature=0, model_name="gpt-4o")
    else:
        raise ValueError(f"Unsupported model type: {model_name}")

    model = model.bind_tools(tools)
    return model

# Define the function that determines whether to continue or not
def should_continue(state):
    messages = state["messages"]
    last_message = messages[-1]
    # If there are no tool calls, then we finish
    if not last_message.tool_calls:
        return "end"
    # Otherwise if there is, we continue
    else:
        return "continue"


system_prompt = """Be a helpful assistant"""

# Define the function that calls the model
def call_model(state, config):
    messages = state["messages"]
    messages = [{"role": "system", "content": system_prompt}] + messages
    model_name = config.get('configurable', {}).get("model_name", "openai")
    model = _get_model(model_name)
    response = model.invoke(messages)
    # We return a list, because this will get added to the existing list
    return {"messages": [response]}

# Define the function to execute tools
tool_node = ToolNode(tools)

# Define the function for generating descriptions
def generate_description(state, config):
    description_prompt = f"Generate a detailed description of the topic around {config['agent']['description_max_words']} words."
    state["messages"].append({"role": "user", "content": description_prompt})
    return call_model(state, config)

# Define the function for generating knowledge graphs
def generate_knowledge_graph(state, config):
    knowledge_graph_prompt = "Generate a knowledge graph for the topic using advanced, styled mermaid.js markdown syntax."
    state["messages"].append({"role": "user", "content": knowledge_graph_prompt})
    return call_model(state, config)

# Define the function for generating related topics
def generate_related_topics(state, config):
