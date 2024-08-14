import asyncio
import os

import typer
import yaml
from langchain.memory import ConversationBufferMemory

from autokb.agent import graph
from autokb.utils.autokb_logging import setup_logging
from autokb.utils.nodes import iterative_refinement, update_agent_config
from autokb.utils.sqlite_db import (clear_tool_responses, initialize_db,
                                    remove_tool_response)
from autokb.utils.state import AgentState

app = typer.Typer()

@app.command()
def generate(
    config_file: str = typer.Option("config.yaml", help="Path to the configuration file"),
):
    """Generate the knowledge base using the specified configuration."""
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)
    
    logger = setup_logging(config)
    logger.info("Starting knowledge base generation...")

    state = AgentState(
        messages=[], 
        covered_topics=set(), 
        topics_queue=[],
        memory=ConversationBufferMemory()
    )
    
    output_dir = config["output"]["working_directory"]
    os.makedirs(output_dir, exist_ok=True)
    
    async def run_generation():
        result = await asyncio.to_thread(graph.run, "description_agent", state)
        refined_result = iterative_refinement(state, config)
        output_path = os.path.join(output_dir, "result.md")
        with open(output_path, "w") as f:
            f.write(refined_result)
        logger.info(f"Knowledge base generated and saved to {output_path}")

    asyncio.run(run_generation())

@app.command()
def configure(config_file: str = typer.Option("config.yaml", help="Path to the configuration file")):
    """Configure the agent by updating the configuration file."""
    typer.echo(f"Loading configuration from {config_file}...")
    with open(config_file, "r") as file:
        config = yaml.safe_load(file)

    # Update config with user inputs
    max_iterations = typer.prompt("Max iterations", default=config["agent"]["max_iterations"])
    retry_attempts = typer.prompt("Retry attempts", default=config["agent"]["retry_attempts"])
    description_max_words = typer.prompt("Max description words", default=config["agent"]["description_max_words"])
    output_dir = typer.prompt("Output directory", default=config["output"]["working_directory"])

    config["agent"]["max_iterations"] = int(max_iterations)
    config["agent"]["retry_attempts"] = int(retry_attempts)
    config["agent"]["description_max_words"] = int(description_max_words)
    config["output"]["working_directory"] = output_dir

    with open(config_file, "w") as file:
        yaml.safe_dump(config, file)

    typer.echo("Configuration updated successfully.")

@app.command()
def cache(action: str = typer.Argument(..., help="Action to perform on cache (clear/remove)"), key: str = typer.Option("", help="Cache key to remove, if action is remove")):
    """Manage the cache."""
    if action == "clear":
        clear_tool_responses()
        typer.echo("Cache cleared.")
    elif action == "remove":
        if key:
            remove_tool_response(int(key))
            typer.echo(f"Cache entry with key '{key}' removed.")
        else:
            typer.echo("Please provide a key to remove.")
    else:
        typer.echo("Invalid action. Use 'clear' or 'remove'.")

if __name__ == "__main__":
    app()

