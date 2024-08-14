from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, Sequence, Set, List, Dict
from langchain.memory import ConversationBufferMemory

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    covered_topics: Set[str]
    topics_queue: List[str]
    memory: ConversationBufferMemory  # Added memory to state
    core_concepts: List[Dict]
    applications: List[Dict]
    resources_tools: List[Dict]
    research_questions: List[Dict]
    historical_context: str
    ethical_considerations: List[Dict]
    future_directions: List[Dict]
