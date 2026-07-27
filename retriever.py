import os
import warnings # <-- 1. Agrega esta línea
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from embeddings import obtener_embeddings

# 2. Agrega esta instrucción para silenciar las advertencias de Excel
warnings.filterwarnings('ignore', category=UserWarning, module='openpyxl')

# Importamos todos los "traductores" de formatos
from langchain_community.document_loaders import (
    PyPDFLoader,
    Docx2txtLoader,
    UnstructuredExcelLoader,
    UnstructuredPowerPointLoader,
    UnstructuredMarkdownLoader,
    UnstructuredHTMLLoader,
    TextLoader
)

def cargar_y_fragmentar_documentos(ruta_carpeta="knowledge_base"):
    """Lee dinámicamente cualquier tipo de archivo soportado en la carpeta y lo corta en fragmentos"""
    documentos = []
    
    if not os.path.exists(ruta_carpeta):
        return None
        
    for archivo in os.listdir(ruta_carpeta):
        ruta_completa = os.path.join(ruta_carpeta, archivo)
        
        try:
            # Elegimos el cargador correcto según la extensión del archivo
            if archivo.endswith(".pdf"):
                loader = PyPDFLoader(ruta_completa)
            elif archivo.endswith(".docx"):
                loader = Docx2txtLoader(ruta_completa)
            elif archivo.endswith(".xlsx"):
                loader = UnstructuredExcelLoader(ruta_completa)
            elif archivo.endswith(".pptx"):
                loader = UnstructuredPowerPointLoader(ruta_completa)
            elif archivo.endswith(".md"):
                loader = UnstructuredMarkdownLoader(ruta_completa)
            elif archivo.endswith(".html"):
                loader = UnstructuredHTMLLoader(ruta_completa)
            elif archivo.endswith(".json"):
                loader = TextLoader(ruta_completa) # Leemos JSON como texto plano
            else:
                continue # Si es un formato no soportado, lo ignora y sigue
                
            documentos.extend(loader.load())
        except Exception as e:
            print(f"No se pudo leer el archivo {archivo}: {e}")
            
    if not documentos:
        return None
        
    # Fragmentamos los documentos en pedazos más pequeños para el Agente
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documentos)
    
    return splits


def configurar_retriever():
    """Configura la base de datos vectorial en memoria RAM"""
    splits = cargar_y_fragmentar_documentos()
    
    if not splits:
        return None
    
    # Creamos la base de datos (sin persist_directory para evitar bloqueos de Windows)
    vectorstore = Chroma.from_documents(
        documents=splits, 
        embedding=obtener_embeddings()
    )
    
    # Configurado para traer los 4 fragmentos más relevantes
    return vectorstore.as_retriever(search_kwargs={"k": 4})