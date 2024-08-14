from pydantic import BaseModel, HttpUrl, Field
from typing import List, Dict

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

class CoreConcept(BaseModel):
    title: str
    definition: str
    importance: str
    related_concepts: List[str]  # List of related core concept titles

class Application(BaseModel):
    title: str
    content: str
    examples: List[str]  # Examples or case studies for the application

class ResourceTool(BaseModel):
    name: str
    description: str
    url: HttpUrl  # Validated URL field

class ResourceToolList(BaseModel):
    tools: List[ResourceTool]

class ResearchQuestion(BaseModel):
    title: str
    content: str

class EthicalConsideration(BaseModel):
    title: str
    description: str
    frameworks_used: List[str]  # Ethical frameworks considered
    stakeholders_affected: List[str]
    mitigation_strategies: List[str]

class FutureDirection(BaseModel):
    title: str
    description: str
    potential_impact: str
    barriers_to_adoption: str
    key_players: List[str]  # Organizations or individuals driving this direction
