import os
from loguru import logger
from rich.console import Console
from rich.logging import RichHandler
from tqdm import tqdm
import langfuse
import langsmith
from dotenv import load_dotenv
from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor

# Load environment variables from .env file
load_dotenv()

# Initialize Rich console
console = Console()

# Initialize langfuse and langsmith with environment variables
langfuse_instance = langfuse.Langfuse(
    secret_key=os.getenv("LANGFUSE_SECRET_KEY"),
    public_key=os.getenv("LANGFUSE_PUBLIC_KEY"),
    host=os.getenv("LANGFUSE_HOST")
)
langsmith.init(api_key=os.getenv("LANGSMITH_API_KEY"))

# Initialize OpenTelemetry tracing
trace_provider = TracerProvider()
trace.set_tracer_provider(trace_provider)
otlp_exporter = OTLPSpanExporter(endpoint=os.getenv("OTLP_ENDPOINT", "http://localhost:4317"))
trace_provider.add_span_processor(BatchSpanProcessor(otlp_exporter))

def setup_logging(config):
    log_level = config.get("logging", {}).get("level", "INFO")
    log_format = config.get("logging", {}).get("format", "{time} - {name} - {level} - {message}")
    log_to_file = config.get("logging", {}).get("log_to_file", True)
    log_file_path = config.get("logging", {}).get("log_file_path", "./logs/agent.log")
    verbosity = config.get("logging", {}).get("verbosity", 1)

    # Remove default logger
    logger.remove()

    # Add RichHandler for console logging
    if verbosity > 0:
        logger.add(RichHandler(console=console, level=log_level, format=log_format))

    # Add file handler for logging to file
    if log_to_file:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        logger.add(log_file_path, level=log_level, format=log_format, rotation="10 MB")

    # Add structured rotating file handler
    logger.add("logs/structured_{time}.json", level=log_level, format=log_format, rotation="10 MB", serialize=True)

    # Add tqdm handler for progress bars
    logger.add(lambda msg: tqdm.write(msg, end=''), level=log_level, format=log_format)

    # Add Langfuse and Langsmith tracing
    langfuse_instance.trace(logger)
    langsmith.trace(logger)

    # OpenTelemetry tracing integration
    tracer = trace.get_tracer(__name__)
    with tracer.start_as_current_span("setup_logging"):
        logger.info("Tracing setup completed")

    return logger
