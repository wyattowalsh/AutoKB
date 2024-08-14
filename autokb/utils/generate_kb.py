import os
from autokb.utils.schema import (
    Description, KnowledgeGraph, RelatedTopics, CoreConcept,
    Application, ResourceToolList, ResearchQuestion, EthicalConsideration,
    FutureDirection
)

def generate_kb_page(description: Description, knowledge_graph: KnowledgeGraph, related_topics: RelatedTopics,
                     core_concepts: List[CoreConcept], applications: List[Application], resources_tools: ResourceToolList,
                     research_questions: List[ResearchQuestion], historical_context: str,
                     ethical_considerations: List[EthicalConsideration], future_directions: List[FutureDirection],
                     output_dir: str):
    """
    Generate a knowledge base page file using the structured data and specified format.
    """
    topic = description.topic
    file_path = os.path.join(output_dir, f"{topic}.md")

    with open(file_path, 'w') as file:
        # Header Section
        file.write(f"# {topic}\n\n")

        # Description Section
        file.write(f"{description.content}\n\n")

        # Knowledge Graph Section
        file.write("## Knowledge Graph\n")
        file.write(f"{generate_knowledge_graph_triplets(knowledge_graph.graph)}\n\n")
        file.write("---\n\n")

        # Core Concepts Section
        file.write("## Core Concepts\n")
        for concept in core_concepts:
            file.write(f"- **{concept.title}**: {concept.definition}\n")
            file.write(f"  - **Importance**: {concept.importance}\n")
            file.write(f"  - **Related Concepts**: {', '.join(concept.related_concepts)}\n\n")
        file.write("---\n\n")

        # Applications Section
        file.write("## Applications\n")
        for application in applications:
            file.write(f"- **{application.title}**: {application.content}\n")
            file.write(f"  - **Examples**: {', '.join(application.examples)}\n\n")
        file.write("---\n\n")

        # Resources & Tools Section
        file.write("## Resources & Tools\n")
        for resource in resources_tools.tools:
            file.write(f"- **[{resource.name}]({resource.url})**: {resource.description}\n\n")
        file.write("---\n\n")

        # Research & Open Questions Section
        file.write("## Research & Open Questions\n")
        for question in research_questions:
            file.write(f"- **{question.title}**: {question.content}\n\n")
        file.write("---\n\n")

        # Historical Context & Key Figures Section
        file.write("## Historical Context & Key Figures\n")
        file.write(f"{historical_context}\n")
        file.write("---\n\n")

        # Ethical Considerations Section
        file.write("## Ethical Considerations\n")
        for ethical_issue in ethical_considerations:
            file.write(f"- **{ethical_issue.title}**: {ethical_issue.description}\n")
            file.write(f"  - **Frameworks Used**: {', '.join(ethical_issue.frameworks_used)}\n")
            file.write(f"  - **Stakeholders Affected**: {', '.join(ethical_issue.stakeholders_affected)}\n")
            file.write(f"  - **Mitigation Strategies**: {', '.join(ethical_issue.mitigation_strategies)}\n\n")
        file.write("---\n\n")

        # Future Directions Section
        file.write("## Future Directions\n")
        for trend in future_directions:
            file.write(f"- **{trend.title}**: {trend.description}\n")
            file.write(f"  - **Potential Impact**: {trend.potential_impact}\n")
            file.write(f"  - **Barriers to Adoption**: {trend.barriers_to_adoption}\n")
            file.write(f"  - **Key Players**: {', '.join(trend.key_players)}\n\n")
        file.write("---\n\n")

        # Related Topics Section
        file.write("## Related Topics\n")
        for related_topic in related_topics.related_topics:
            file.write(f"- [[{related_topic}]]\n")

def generate_knowledge_graph_triplets(triplets: list[SemanticTriple]):
    """
    Generate a knowledge graph using entity-relation semantic triplets and advanced mermaid.js markdown syntax.
    """
    mermaid_syntax = "```mermaid\ngraph TD\n"
    for triplet in triplets:
        mermaid_syntax += f"    {triplet.source} -->|{triplet.relation}| {triplet.target}\n"
    mermaid_syntax += "```\n"
    return mermaid_syntax
