import google.generativeai as genai
import my_keys

# Nos conectamos con tu clave
genai.configure(api_key=my_keys.GOOGLE_API_KEY)

print("Conectando con Google para verificar tus modelos de TEXTO...")

try:
    # Filtramos solo los modelos que sirven para conversar y redactar (generateContent)
    modelos_texto = [
        m.name for m in genai.list_models() 
        if 'generateContent' in m.supported_generation_methods
    ]
    
    if modelos_texto:
        print("\n¡Éxito! Tu clave puede usar estos modelos de lenguaje (LLM):")
        for modelo in modelos_texto:
            print(f" -> {modelo}")
    else:
        print("\nTu clave no tiene permisos para generar texto.")
        
except Exception as e:
    print(f"\n❌ Error: {e}")