import streamlit as st
# from schneider_chatbot.chatbot.initialization import initialize_vertex_ai, get_llm, get_embedding_model
from schneider_chatbot.chatbot.llm_initialization import get_llm
# from schneider_chatbot.chatbot.vector_store import initialize_vector_store, get_retriever
from schneider_chatbot.chatbot.prompts import get_contextualize_question_prompt, get_qa_prompt
from schneider_chatbot.chatbot.chains import create_history_aware_chain, create_qa_chain, create_rag_chain
from schneider_chatbot.chatbot.session_management import generate_session_id, get_session_history, create_conversational_rag_chain
from schneider_chatbot.chatbot.llama_retriever import LlamaQueryEngineRetriever, create_llamaindex_retriever
# Initialize Vertex AI
# initialize_vertex_ai()

# Initialize Models
llm = get_llm()
# embedding_model = get_embedding_model()

# # Initialize Vector Store and Retriever
# vector_store = initialize_vector_store(embedding_model)
# retriever = get_retriever(vector_store)

# Initialize Vector Store and Retriever
from llama_index.indices.managed.llama_cloud import LlamaCloudIndex
# pip install llama-index-indices-managed-llama-cloud

retriever = create_llamaindex_retriever()

print(type(retriever))
# Prompts
contextualize_q_prompt = get_contextualize_question_prompt()
qa_prompt = get_qa_prompt()

# Create Chains
history_aware_retriever_chain = create_history_aware_chain(llm, retriever, contextualize_q_prompt)

question_answer_chain = create_qa_chain(llm, qa_prompt)
rag_chain = create_rag_chain(history_aware_retriever_chain, question_answer_chain)

# Session Management
session_id = generate_session_id()
conversational_rag_chain = create_conversational_rag_chain(rag_chain, get_session_history)

# # Streamlit App
# st.title("Conversational RAG Application")
# user_input = st.text_input("Enter your query:")
# if st.button("Submit"):
#     response = conversational_rag_chain.invoke(
#         {"input": user_input},
#         config={"configurable": {"session_id": session_id}},
#     )
#     st.write(response["answer"])
