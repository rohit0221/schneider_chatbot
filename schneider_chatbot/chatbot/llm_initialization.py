import vertexai
from langchain_google_vertexai import VertexAI, VertexAIEmbeddings

from langchain_openai import ChatOpenAI

from configs.config import VERTEX_AI_PROJECT, VERTEX_AI_LOCATION, GEN_AI_MODEL_PROVIDER,OPEN_AI_MODEL,GEMINI_MODEL

def initialize_vertex_ai():
    vertexai.init(project=VERTEX_AI_PROJECT, location=VERTEX_AI_LOCATION)

def get_llm():
    # return VertexAI(model_name=GEN_AI_MODEL, verbose=True)
    return ChatOpenAI(model="gpt-4o-mini")


import os
from langchain.chat_models import ChatOpenAI
from langchain_google_vertexai import VertexAI
import vertexai

def get_llm():
    """
    Returns an LLM instance based on the value of GEN_AI_MODEL.
    
    If GEN_AI_MODEL is "gpt-4o-mini" or any OpenAI model, it returns ChatOpenAI.
    If GEN_AI_MODEL is "gemini-pro" or any Gemini model, it initializes Vertex AI and returns VertexAI.
    """
    if GEN_AI_MODEL_PROVIDER=="openai":
        # Use OpenAI model
        return ChatOpenAI(model=OPEN_AI_MODEL, verbose=True)
    
    elif GEN_AI_MODEL_PROVIDER=="google":
        initialize_vertex_ai()
        # Initialize Vertex AI client
        vertexai.init(project=VERTEX_AI_PROJECT, location=VERTEX_AI_LOCATION)        
        return VertexAI(model_name=GEMINI_MODEL, verbose=True)
    
    else:
        raise ValueError(f"Unsupported model provider: {GEN_AI_MODEL_PROVIDER}")

# def get_embedding_model():
#     return VertexAIEmbeddings(model_name=EMBEDDING_MODEL_NAME)
