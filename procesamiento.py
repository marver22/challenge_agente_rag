from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def cargar_y_fragmentar_documentos(ruta_carpeta="knowledge_base"):
    if not os.path.exists(ruta_carpeta):
        os.makedirs(ruta_carpeta)
        return []
    
    loader = PyPDFDirectoryLoader(ruta_carpeta)
    docs = loader.load()
    
    if not docs:
        return []
        
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)
    return splits