<h1 align="center">🤖 Agente RAG Corporativo</h1>

<p align="center">
  <strong>Un Asistente Inteligente de Documentos impulsado por Inteligencia Artificial</strong><br>
  <em>Desarrollado para el Challenge de Alura - Oracle Next Education</em>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12-blue?style=for-the-badge&logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white" alt="Streamlit">
  <img src="https://img.shields.io/badge/LangChain-121212?style=for-the-badge&logo=chainlink&logoColor=white" alt="LangChain">
  <img src="https://img.shields.io/badge/Google_Gemini-8E75B2?style=for-the-badge&logo=google&logoColor=white" alt="Gemini">
  <img src="https://img.shields.io/badge/ChromaDB-FF6F00?style=for-the-badge&logo=database&logoColor=white" alt="ChromaDB">
</p>

<hr>

## 📖 Sobre el Proyecto

Este proyecto es un chatbot corporativo interactivo y dinámico construido con Inteligencia Artificial. Su principal objetivo es leer, analizar y responder preguntas basadas **exclusivamente en los documentos que el usuario sube en tiempo real**.

Utiliza la arquitectura **RAG (Retrieval-Augmented Generation)** para garantizar que las respuestas sean 100% precisas, eliminando las "alucinaciones" de la IA y respaldando cada dato con citas directas a los documentos originales.

---

## ✨ Características Principales

- **📂 Carga Multiformato Dinámica:** Soporta archivos `.pdf`, `.docx`, `.xlsx`, `.pptx`, `.md`, `.json` y `.html`.
- **🛡️ Privacidad y Seguridad In-Memory:** Los documentos y la base de datos vectorial viven en la memoria RAM. Al cerrar la sesión, todo desaparece. 
- **❌ Gestión de Archivos en Tiempo Real:** Interfaz intuitiva para eliminar archivos individuales al vuelo, reconfigurando el "cerebro" del bot instantáneamente.
- **🔍 Trazabilidad Absoluta:** Cada respuesta incluye un pie de página indicando la fuente exacta (Documento y Página) de donde se extrajo la información.
- **🚦 Control Anti-Saturación (Rate Limits):** Escudo protector (`try-except`) que maneja inteligentemente los límites de cuota de la API gratuita, ofreciendo una experiencia de usuario fluida sin errores de consola.

---

## 🏗️ Arquitectura de la Solución

```text
┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│                  │      │  Orquestador     │      │                  │
│    Streamlit     │─────►│  (LangChain)     │─────►│ Google Gemini API│
│ (Frontend & UI)  │ HTTP │   Pipeline RAG   │      │  (LLM & Embed.)  │
└──────────────────┘      └────────┬─────────┘      └──────────────────┘
                                   │
                          ┌────────▼────────┐ 
                          │                 │ 
                          │    ChromaDB     │ 
                          │  (In-Memory)    │ 
                          │                 │ 
                          └─────────────────┘

```
---

### 🔄 Flujo de trabajo:
1. El usuario sube sus documentos desde el panel lateral.
2. El sistema fragmenta los textos, los convierte en vectores matemáticos (Embeddings) y los indexa en ChromaDB.
3. El usuario realiza una consulta en lenguaje natural.
4. El Agente recupera el contexto más relevante, lo inyecta en el modelo Gemini y devuelve una respuesta fundamentada con sus respectivas referencias.

---

## 💻 Stack Tecnológico

| Componente | Tecnología | Descripción |
| :--- | :--- | :--- |
| **Lenguaje Core** | `Python 3.12` | Base del desarrollo del proyecto. |
| **Frontend UI** | `Streamlit` | Creación de la interfaz gráfica web interactiva. |
| **Framework IA**| `LangChain` | Orquestación del flujo RAG y manejo de prompts. |
| **Base de Datos**| `ChromaDB` | Base de datos vectorial volátil. |
| **Embeddings** | `Google Generative AI` | Representación vectorial semántica del texto. |
| **LLM** | `Google Gemini Flash` | Motor de generación de respuestas inteligentes. |
---
## 📂 Estructura del Repositorio

```text
CHALLENGE_AGENTE_RAG/
├── knowledge_base/       # (Ignorado en Git) Carpeta temporal de archivos subidos
├── venv/                 # (Ignorado en Git) Entorno virtual
├── .gitignore            # Archivos y carpetas excluidos del control de versiones
├── app.py                # Interfaz principal (Streamlit) y manejo de sesión
├── embeddings.py         # Configuración del modelo de Embeddings
├── llm.py                # Conexión con el modelo Gemini de Google
├── my_keys.py            # (Ignorado en Git) Variables de entorno y API Keys
├── orquestador.py        # Ensamblaje de la cadena RAG
├── retriever.py          # Lógica de carga multiformato y base vectorial
└── requirements.txt      # Dependencias del proyecto
```
---
## 🚀 Guía de Instalación y Uso

Sigue estos pasos para ejecutar el proyecto en tu máquina local:

### 1. Clonar el repositorio
```bash
git clone [https://github.com/marver22/challenge_agente_rag.git]
cd challenge_agente_rag
```

### 2. Configurar el entorno virtual
```bash
python -m venv venv

# Activar en Windows:
source venv/Scripts/activate

# Activar en Mac/Linux:
source venv/bin/activate
```

### 3. Instalar las dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar las credenciales (API Key)
Crea un archivo llamado `my_keys.py` en la raíz del proyecto y añade tu clave gratuita de Google AI Studio:

```python
import os
os.environ["GOOGLE_API_KEY"] = "TU_CLAVE_API_AQUI"
```

### 5. Iniciar la aplicación
```bash
python -m streamlit run app.py
```
> 🌐 La aplicación se abrirá automáticamente en tu navegador web en `http://localhost:8501`.

---

## 💬 Ejemplo de Interacción

**1. Acción:** Sube el documento `politicas_vacaciones.pdf` usando el panel lateral y haz clic en "Procesar Documentos".

**2. Consulta:** *"¿Cuántos días me corresponden si llevo 2 años en la empresa?"*

**3. Respuesta del Asistente:** 
> "De acuerdo con las políticas de la empresa, los empleados con 2 años de antigüedad tienen derecho a 15 días hábiles de vacaciones remuneradas.
> 
> ---
> **📚 Fuentes consultadas:**
> - politicas_vacaciones.pdf (Pág. 3)"

---

## ☁️ Deploy

**Enlace público:** [http://192.168.0.16:8501](http://192.168.0.16:8501)

**Imagen de funcionamiento:**
<!-- Reemplaza "URL_DE_TU_GIF_AQUI" con el enlace real a tu imagen o bórralo si aún no lo tienes -->
<img width="1348" height="587" alt="Agente RAG" src="https://github.com/user-attachments/assets/00d90ed7-d0f3-408d-aa0a-643fc2f83857" />
