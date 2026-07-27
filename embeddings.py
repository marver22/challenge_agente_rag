from langchain_google_genai import GoogleGenerativeAIEmbeddings
try:
    import my_keys
    except ImportError:
        pass

def obtener_embeddings():
    # Utilizamos el modelo exacto al que tu API Key tiene acceso según el diagnóstico
    return GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-2")