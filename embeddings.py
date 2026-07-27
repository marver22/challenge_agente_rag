from langchain_google_genai import GoogleGenerativeAIEmbeddings
import my_keys 

def obtener_embeddings():
    # Utilizamos el modelo exacto al que tu API Key tiene acceso según el diagnóstico
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")