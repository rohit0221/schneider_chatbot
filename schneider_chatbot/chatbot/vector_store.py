# from google.cloud import aiplatform
# from langchain_google_vertexai import VectorSearchVectorStore
# from configs.config import VERTEX_AI_PROJECT, VERTEX_AI_LOCATION, BUCKET, INDEX_NAME, INDEX_ENDPOINT

# def initialize_vector_store(embedding_model):
#     my_index = aiplatform.MatchingEngineIndex(INDEX_NAME)
#     my_index_endpoint = aiplatform.MatchingEngineIndexEndpoint(INDEX_ENDPOINT)

#     vector_store = VectorSearchVectorStore.from_components(
#         project_id=VERTEX_AI_PROJECT,
#         region=VERTEX_AI_LOCATION,
#         gcs_bucket_name=BUCKET,
#         index_id=my_index.name,
#         endpoint_id=my_index_endpoint.name,
#         embedding=embedding_model,
#     )

#     return vector_store

# def get_retriever(vector_store):
#     return vector_store.as_retriever()
