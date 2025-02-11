from langchain.chains import create_history_aware_retriever,create_retrieval_chain

from langchain.chains.combine_documents import create_stuff_documents_chain

# def create_history_aware_chain(llm, retriever, contextualize_q_prompt):
#     return create_history_aware_retriever(llm, retriever, contextualize_q_prompt)

def create_history_aware_chain(llm, retriever, contextualize_q_prompt):
    print("Inside create_history_aware_chain")
    print("Type of retriever:", type(retriever))
    print("Calling create_history_aware_retriever...")

    try:
        history_aware_retriever = create_history_aware_retriever(llm, retriever, contextualize_q_prompt)
        print("Type of history_aware_retriever:", type(history_aware_retriever))
    except Exception as e:
        print("Error inside create_history_aware_retriever:", str(e))
        raise

    return history_aware_retriever



def create_qa_chain(llm, qa_prompt):
    return create_stuff_documents_chain(llm, qa_prompt)

def create_rag_chain(history_aware_retriever_chain, question_answer_chain):
    return create_retrieval_chain(history_aware_retriever_chain, question_answer_chain)
