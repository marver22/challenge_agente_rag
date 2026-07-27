from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from llm import obtener_llm
from retriever import configurar_retriever

def crear_agente_rag():
    retriever = configurar_retriever()
    if not retriever:
        return None

    llm = obtener_llm()

    system_prompt = (
        "Eres un asistente corporativo experto en las políticas internas de la empresa. "
        "Responde a las preguntas de los colaboradores utilizando EXCLUSIVAMENTE los siguientes fragmentos recuperados. "
        "Si la respuesta no está en el contexto, di: 'Lo siento, no encuentro información sobre ese tema en las políticas actuales'. "
        "Nunca inventes información.\n\n"
        "Contexto recuperado: {context}"
    )
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        ("human", "{input}"),
    ])
    
    question_answer_chain = create_stuff_documents_chain(llm, prompt)
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    return rag_chain