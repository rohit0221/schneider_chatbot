import os
from dotenv import load_dotenv

def initialize_langsmith():
    """
    Initializes LangSmith tracing by loading environment variables from a .env file
    and ensuring they are properly set in the runtime environment.
    """
    # Load environment variables from .env file if present
    load_dotenv()

    os.environ["LANGCHAIN_API_KEY"]=os.environ.get('LANGCHAIN_API_KEY')
    os.environ["LANGSMITH_ENDPOINT"]=os.environ.get('LANGSMITH_ENDPOINT')
    os.environ["LANGCHAIN_TRACING_V2"]=os.environ.get('LANGCHAIN_TRACING_V2')
    os.environ["LANGCHAIN_PROJECT"]=os.environ.get('LANGCHAIN_PROJECT')

    # Validate that the API key is set
    if not os.environ["LANGCHAIN_API_KEY"]:
        raise ValueError("LANGCHAIN_API_KEY is not set. Please provide a valid API key.")

    print("✅ LangSmith tracing initialized successfully!")

# Call the function at the start of your script
