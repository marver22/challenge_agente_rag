from langchain_google_genai import ChatGoogleGenerativeAI
#import my_keys
try:
    import my_keys
except ImportError:
    pass
def obtener_llm():
    # Insertamos el modelo Pro estable al que tienes acceso
    return ChatGoogleGenerativeAI(model="models/gemini-3.5-flash")