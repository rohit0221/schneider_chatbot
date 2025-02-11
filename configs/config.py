import os
from dotenv import load_dotenv

# Load environment variables from .env file if running locally
if os.getenv("ENV") == "LOCAL":  # Only load dotenv if running locally
    load_dotenv()

# Read environment variables directly
LOG_LEVEL_CONSOLE = os.getenv("LOG_LEVEL_CONSOLE").upper()
LOG_LEVEL_FILE = os.getenv("LOG_LEVEL_FILE").upper()
VERTEX_AI_PROJECT= os.getenv("VERTEX_AI_PROJECT")
VERTEX_AI_LOCATION= os.getenv("VERTEX_AI_LOCATION")
GEN_AI_MODEL_PROVIDER= os.getenv("GEN_AI_MODEL_PROVIDER")
OPEN_AI_MODEL= os.getenv("OPEN_AI_MODEL")
GEMINI_MODEL= os.getenv("GEMINI_MODEL")

# BUCKET= os.getenv("BUCKET")

# EMBEDDING_MODEL_NAME= os.getenv("EMBEDDING_MODEL_NAME")
# INDEX_NAME= os.getenv("INDEX_NAME")
# INDEX_ENDPOINT= os.getenv("INDEX_ENDPOINT")


# API Keys
LLAMA_CLOUD_API_KEY = os.getenv("LLAMA_CLOUD_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY")

# LangChain Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT")
LANGSMITH_ENDPOINT = os.getenv("LANGSMITH_ENDPOINT")

# Llama Index Configuration
LLAMA_INDEX_NAME = os.getenv("LLAMA_INDEX_NAME")
LLAMA_PROJECT_NAME = os.getenv("LLAMA_PROJECT_NAME")
LLAMA_ORG_ID = os.getenv("LLAMA_ORG_ID")
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")