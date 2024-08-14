from langgraph.graph import add_messages
from langchain_core.messages import BaseMessage
from typing import TypedDict, Annotated, Sequence, Set, List

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    covered_topics: Set[str]
    topics_queue: List[str]
