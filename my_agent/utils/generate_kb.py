import os
from my_agent.utils.schema import Description, KnowledgeGraph, RelatedTopics, SemanticTriple

def generate_kb_page(description: Description, knowledge_graph: KnowledgeGraph, related_topics: RelatedTopics, output_dir: str):
    """
    Generate a knowledge base page file using the structured data and specified format.
    """
    topic = description.topic
    file_path = os.path.join(output_dir, f"{topic}.md")

    with open(file_path, 'w') as file:
        file.write(f"# {topic}\n\n")
        file.write(f"{description.content}\n\n")
        file.write(f"{generate_knowledge_graph_triplets(knowledge_graph.graph)}\n\n")
        file.write("---\n\n")
        file.write("## Related Topics\n\n")
        for related_topic in related_topics.related_topics:
            file.write(f"- [[{related_topic}]]\n")

def generate_knowledge_graph_triplets(triplets: list[SemanticTriple]):
    """
    Generate a knowledge graph using entity relation semantic triplets and mermaid.js markdown syntax.
    """
    mermaid_syntax = "```mermaid\ngraph TD\n"
    for triplet in triplets:
        mermaid_syntax += f"    {triplet.source} -->|{triplet.relation}| {triplet.target}\n"
    mermaid_syntax += "```"
    return mermaid_syntax
