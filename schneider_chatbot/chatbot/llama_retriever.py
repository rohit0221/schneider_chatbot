from langchain.schema import Document
from langchain_core.retrievers import BaseRetriever
from pydantic import Field
from typing import Any, Dict, List
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
from langchain_community.retrievers.llama_index import LlamaIndexRetriever

from configs.config import LLAMA_INDEX_NAME, LLAMA_PROJECT_NAME, LLAMA_ORG_ID,LLAMA_API_KEY

class LlamaQueryEngineRetriever(BaseRetriever):
    """
    A LangChain retriever that wraps a LlamaIndex query engine.
    """

    query_engine: Any = None  # The LlamaIndex query engine

    def _get_relevant_documents(self, query: str, *, run_manager=None) -> List[Document]:
        # Run the query through the LlamaIndex query engine
        response = self.query_engine.query(query)

        # Convert the LlamaIndex response into LangChain Documents
        docs = []
        for source_node in response.source_nodes:
            metadata = source_node.metadata or {}
            docs.append(Document(page_content=source_node.get_content(), metadata=metadata))

        return docs


# from langchain_community.retrievers.llama_index import LlamaIndexRetriever, LlamaQueryEngineRetriever
# from llama_index import LlamaCloudIndex

def create_llamaindex_retriever():
    """
    Creates and returns a retriever using LlamaCloudIndex and LlamaQueryEngineRetriever.
    
    Returns:
        retriever: A retriever instance for querying the LlamaCloudIndex.
    """
    # Define the index
    index = LlamaCloudIndex(
        name=LLAMA_INDEX_NAME,
        project_name=LLAMA_PROJECT_NAME,
        organization_id=LLAMA_ORG_ID,
        api_key=LLAMA_API_KEY
    )

    # Create the query engine
    query_engine = index.as_query_engine(query_kwargs={})
    print(type(query_engine))
    # Create and return the retriever
    retriever = LlamaQueryEngineRetriever(query_engine=query_engine)
    print(type(retriever))
    return retriever
