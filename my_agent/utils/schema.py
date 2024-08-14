from pydantic import BaseModel
from typing import List

class Description(BaseModel):
    topic: str
    content: str

class SemanticTriple(BaseModel):
    source: str
    target: str
    relation: str

class KnowledgeGraph(BaseModel):
    topic: str
    graph: List[SemanticTriple]

class RelatedTopics(BaseModel):
    topic: str
    related_topics: List[str]
