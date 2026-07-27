import streamlit as st
import os
import shutil
import os

try:
    import my_keys
    except ImportError:
        pass
        
from orquestador import crear_agente_rag 

# Configuración inicial de la página
st.set_page_config(page_title="Intranet - Políticas de Empresa", page_icon="🏢")

# 1. Diseñar el Panel Izquierdo (Sidebar)
with st.sidebar:
    st.header("📂 Sube tus archivos aquí")
    st.write("Sube tus documentos para que el asistente los analice. Al cerrar la app, todo se borrará por seguridad.")
    
    # Ampliamos los formatos permitidos
    formatos_soportados = ["pdf", "docx", "xlsx", "pptx", "md", "json", "html"]
    archivos_subidos = st.file_uploader("Selecciona tus archivos", type=formatos_soportados, accept_multiple_files=True)
    btn_procesar = st.button("Procesar Documentos")
    
    st.markdown("---")
    st.subheader("📄 En la memoria del Bot:")
    
    # --- MEJORA 1: Lógica para mostrar archivos con botón de eliminar (❌) ---
    if os.path.exists("knowledge_base") and os.listdir("knowledge_base"):
        for doc in os.listdir("knowledge_base"):
            # Dividimos el espacio para que el nombre y la X estén en la misma línea
            col1, col2 = st.columns([0.8, 0.2])
            with col1:
                st.write(f"✅ {doc}")
            with col2:
                # Botón individual para eliminar
                if st.button("❌", key=f"del_{doc}"):
                    # Borramos el archivo físico
                    os.remove(os.path.join("knowledge_base", doc))
                    
                    # Reconstruimos la memoria del Agente
                    if os.listdir("knowledge_base"): 
                        st.session_state.agente = crear_agente_rag()
                    else:
                        st.session_state.agente = None # Apagamos el bot si ya no hay archivos
                    
                    # Forzamos a Streamlit a recargar la página al instante
                    st.rerun()
    else:
        st.write("No hay documentos cargados en esta sesión.")

# 2. Lógica para procesar cuando se presiona el botón
if btn_procesar and archivos_subidos:
    with st.spinner("Procesando e indexando tus documentos..."):
        
        # Para evitar mezclar documentos viejos con nuevos, vaciamos la carpeta anterior
        #if os.path.exists("knowledge_base"):
        #    shutil.rmtree("knowledge_base")
        #os.makedirs("knowledge_base") # La volvemos a crear limpia
        
        # Borramos la base de datos vectorial vieja para que no haya datos fantasma
        if os.path.exists("chroma_db"):
            shutil.rmtree("chroma_db")
        
        # Guardamos cada archivo que subiste desde la web hacia tu disco duro
        for archivo in archivos_subidos:
            ruta_guardado = os.path.join("knowledge_base", archivo.name)
            with open(ruta_guardado, "wb") as f:
                f.write(archivo.getbuffer())
        
        # Ahora que los archivos están en su lugar, encendemos el agente de LangChain
        st.session_state.agente = crear_agente_rag()
        st.success("¡Documentos cargados y listos para consultar!")

elif btn_procesar and not archivos_subidos:
    st.sidebar.warning("Por favor, sube al menos un documento antes de procesar.")

# 3. Diseño del Chat Principal (Centro de la pantalla)
st.title("💬 Agente Corporativo Industrial")

# Verificar si el agente ya fue creado en esta sesión
if "agente" not in st.session_state or st.session_state.agente is None:
    st.info("""
    👋 **¡Bienvenido a la demostración del Agente RAG!**
    
    Para comenzar a evaluar el asistente, por favor sigue estos pasos:
    1. Ve al panel izquierdo y sube tus documentos de prueba.
    2. Puedes probar con formatos como: **PDF, Word, Excel, PowerPoint, Markdown, HTML o JSON**.
    3. Haz clic en **'Procesar Documentos'**.
    
    *Nota: Por seguridad y privacidad, todos los documentos se eliminarán automáticamente al finalizar la sesión.*
    """)
else:
    # 1. Inicializar el historial de mensajes si no existe
    if "mensajes" not in st.session_state:
        st.session_state.mensajes = []

    # 2. Mostrar el historial de conversación en pantalla
    for mensaje in st.session_state.mensajes:
        with st.chat_message(mensaje["rol"]):
            st.markdown(mensaje["contenido"])

    # --- MEJORA 2: CAJA DE TEXTO (Asegurada dentro del bloque else) ---
    pregunta = st.chat_input("Escribe tu pregunta sobre los documentos...")

    # 4. Lógica de respuesta
    if pregunta:
        # Mostrar la pregunta del usuario en el chat
        with st.chat_message("user"):
            st.markdown(pregunta)
        
        # Guardar en historial
        st.session_state.mensajes.append({"rol": "user", "contenido": pregunta})

        # Obtener respuesta de Gemini
        with st.chat_message("assistant"):
            with st.spinner("Analizando documentos..."):
                try:
                    # INTENTAMOS: Enviar la pregunta a la cadena RAG
                    respuesta = st.session_state.agente.invoke({"input": pregunta})
                    
                    texto_respuesta = respuesta["answer"]
                    documentos_origen = respuesta["context"] 
                    
                    # Lógica para extraer las fuentes (Metadata)
                    texto_fuentes = "\n\n---\n**📚 Fuentes consultadas:**\n"
                    fuentes_vistas = set() 
                    
                    for doc in documentos_origen:
                        ruta_completa = doc.metadata.get("source", "Documento desconocido")
                        nombre_archivo = os.path.basename(ruta_completa)
                        
                        pagina = doc.metadata.get("page")
                        
                        if pagina is not None:
                            etiqueta = f"- {nombre_archivo} (Pág. {pagina + 1})"
                        else:
                            etiqueta = f"- {nombre_archivo}"
                            
                        if etiqueta not in fuentes_vistas:
                            fuentes_vistas.add(etiqueta)
                            texto_fuentes += etiqueta + "\n"
                    
                    # Unimos la respuesta de Gemini con las fuentes
                    respuesta_final = texto_respuesta + texto_fuentes
                    
                    # Mostramos en pantalla
                    st.markdown(respuesta_final)
            
                    # Guardar la respuesta final completa en el historial
                    st.session_state.mensajes.append({"rol": "assistant", "contenido": respuesta_final})

                except Exception as e:
                    # ATRAPAMOS EL ERROR: Si Google rechaza la petición por ir muy rápido
                    error_msg = str(e).lower()
                    if "429" in error_msg or "resourceexhausted" in error_msg or "quota" in error_msg:
                        st.warning("⏳ ¡Vaya, vas muy rápido! El servidor necesita un pequeño respiro. Por favor, espera unos 30 segundos y vuelve a intentar tu pregunta.")
                    else:
                        st.error(f"❌ Ocurrió un error al procesar el documento. Intenta nuevamente.")
                    
                    # Como hubo un error y el bot no respondió, borramos tu pregunta del historial 
                    # para que la pantalla no se llene de preguntas sin respuesta
                    st.session_state.mensajes.pop()