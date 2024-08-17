# autokb

A LangGraph multi-agent LLM system for automatic knowledge base generation. The system should be able to generate new knowledge bases based on an input list of seed topics and also continue existing knowledge bases (also with an optional input list of seed topics). For new knowledge base generation, the system should conduct research on the topic using a collection of search tools and then generate knowledge base pages for each seed topic. The knowledge base pages should follow this template:

```md
---
title: <topic (Title Capitalization: first letter capital of every major word )>
tags: <distilled list of most associated keywords>
aliases: <list of alternative names or spellings>
created: <created datetime in the form: 2024-08-09T01:30>
updated: <updated datetime in the form: 2024-08-09T01:32>
---

# <topic (Title Capitalization)>

<topic description: a robust, comprehensive, and maximally well written description for the page topic geared towards an audience of post-doctoral technical research fellows and around 1000 words in length. Obsidian markdown format should be used including latex for equations using $ or $$. The description should be intelligently structured for optimized readability>

<topical knowledge graph: mermaid.js markdown knowledge graph maximally representative of the topic based on triples (all arcs should be labeled). The knowledge graph should be intelligently stylized for optimized readability and usefulness>

---

## Related Topics

<list of top 25 most related topics: bulleted list of the top 25 most related topics to the page topic where the page topics are in title capitalization (similar to the page title) and wikilinks syntax (surround by double brackets [[Related Topic Example]])>

---

## Resources

<comprehensive, robust, up-to-date list of related resources: each resource should have a useful description, associated links, and other helpful info. The list should be sorted and categorized>

```

Once all input seed topics have had their knowledge base pages generated, knowledge base pages should be generated for all unique related topics that are not yet in the knowledge base. After generating the pages for all the unique related topics related to the input seed topics, any new related topics across the generated pages should have their knowledge base pages generated. This process should continue until no new related topics are generated or an input limit is reached. When continuing an existing knowledge base, the system should generate knowledge base pages for all unique related topics that are not yet in the knowledge base, conducting research on each topic using a collection of search tools. After generating the pages for all the unique related topics related to the existing knowledge base, any new related topics across the generated pages should have their knowledge base pages generated. This process should continue until no new related topics are generated or an input limit is reached.

## Tool Stack

| Tool            | Purpose                                                                 |
|-----------------|-------------------------------------------------------------------------|
| Python          | Scripting                                                               |
| LangGraph       | Multi-Agent LLM Orchestration                                           |
| LangChain       | LLM Systems                                                             |
| LlamaIndex      | LLM Systems                                                             |
| LangFuse        | LLM Monitoring                                                          |
| LangSmith       | LLM Monitoring                                                          |
| Loguru + Rich   | Logging and rich text formatting                                        |
| Typer           | Command-line interface creation                                         |
| FastAPI         | Framework for Websocket Implementation                                  |
| Pydantic        | Data validation and settings management using Python type annotations   |
| Tenacity        | Retrying library for Python                                             |
| pyenv           | Python version management                                               |
| poetry          | Python dependency management and packaging                              |
| LangGraph Studio| GUI for Multi-Agent LLM Orchestration                                   |


## Agents

All LLM systems should only use OpenAI GPT-4o for their language model. The following tools will be used by the agents:

- Tavily Search
- Serper
- Arxiv
- Wikipedia
- Wikidata
- Reddit Search
- Exa Search
- StackExchange

The following agents will be used:

- Researchers: Conducts research on a topic using a search tool
    - one researcher per search tool
      - intelligent, well crafted, robust search query generation
      - output synthesis, distillation, and summarization
    - one 'manager' researcher to manage the other researchers
      - compiles output for input to data generator
    - Structured IO
- Page Data Generator: Generates JSON data for a knowledge base page based on the researcher's findings
  - Structured IO
    - JSON mode