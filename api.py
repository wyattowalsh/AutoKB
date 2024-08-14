from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import yaml
import asyncio
import logging
from my_agent.agent import graph
from my_agent.utils.state import AgentState
from my_agent.utils.kbgen_logging import setup_logging

app = FastAPI()

# Load configuration
with open("config.yaml", "r") as file:
    config = yaml.safe_load(file)

# Setup logging
logger = setup_logging(config)

# Configure CORS
origins = config["websocket_api"]["allowed_origins"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    state = AgentState(messages=[], covered_topics=set(), topics_queue=[])
    try:
        while True:
            data = await websocket.receive_text()
            config_update = yaml.safe_load(data)
            config.update(config_update)
            logger.info(f"Configuration updated: {config_update}")

            # Run the knowledge base generation
            result = await asyncio.to_thread(graph.run, "description_agent", state)
            await websocket.send_text(result)
            logger.info(f"Result sent: {result}")

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"Error: {e}")
        await websocket.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=config["websocket_api"]["host"], port=config["websocket_api"]["port"], log_level=config["websocket_api"]["log_level"])
