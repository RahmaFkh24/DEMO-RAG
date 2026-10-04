# TechCorp Employee Handbook — RAG Application

A local Retrieval-Augmented Generation (RAG) application that uses a PDF employee handbook to answer questions through Google Gemini and a Gradio interface.

## Requirements

* **Python:** 3.11 or later
* **Google Gemini API key:** Access to the configured embedding and chat models
* **Handbook PDF:** `TechCorp_Official_Employee_Handbook.pdf`
* **Internet connection:** Required for Gemini API requests

## Setup on Windows

### 1. Create a Virtual Environment

Open PowerShell in the project directory and run:

```powershell
py -m venv venv
```

### 2. Install Dependencies

Install the required Python packages:

```powershell
.\venv\Scripts\python.exe -m pip install gradio python-dotenv langchain-community langchain-text-splitters langchain-google-genai chromadb pypdf
```

### 3. Add the Handbook PDF

Place the following file in the project directory, alongside `rag_app.py`:

```text
TechCorp_Official_Employee_Handbook.pdf
```

Make sure the filename matches exactly.

### 4. Configure the Gemini API Key

Create a `.env` file in the project directory and add your Google Gemini API key:

```dotenv
GOOGLE_API_KEY=your-google-gemini-api-key
```

**Security note:** Keep your `.env` file private. Never commit or share your API key. Add `.env` and other sensitive files to `.gitignore`.

## Run the Application

From the project directory, execute:

```powershell
.\venv\Scripts\python.exe rag_app.py
```

Wait for Gradio to start. The terminal will display a local URL, usually:

**http://127.0.0.1:7860**

Open this URL in your web browser to use the application.

To stop the application, press **Ctrl + C** in PowerShell.

## Project Structure

The project directory should contain the following files and folders:

```text
project/
├── rag_app.py
├── TechCorp_Official_Employee_Handbook.pdf
├── .env
├── .gitignore
├── venv/
└── chroma_db/
```

* `rag_app.py` — Main application.
* `TechCorp_Official_Employee_Handbook.pdf` — Source document used for question answering.
* `.env` — Stores the Gemini API key.
* `venv/` — Python virtual environment.
* `chroma_db/` — Local vector database created by the application, if persistence is enabled.

## Notes

* **PDF location:** The PDF path is currently configured directly in `rag_app.py`. The file must have the expected name and be accessible from the application's working directory.
* **Vector database:** ChromaDB data is stored locally in `./chroma_db`, provided the application is configured for persistent storage.
* **Gemini API:** The application uses Google Gemini for text embeddings and generated answers. A valid API key, model access, and internet connectivity are required.
* **Local access:** Gradio runs locally by default. Avoid enabling public sharing unless you intentionally want to expose the interface.
* **Python environment:** Run the application using the virtual environment to ensure that the required dependencies are available.

## Troubleshooting

**Python is not recognized**

Check that Python 3.11 or later is installed:

```powershell
py --version
```

**Missing dependencies**

Reinstall the packages using the installation command above.

**API key errors**

Verify that `.env` exists in the project directory, that `GOOGLE_API_KEY` is spelled correctly, and that your API key has access to the configured Gemini models.

**PDF not found**

Check the PDF filename and ensure that the file is in the expected directory.

**Port already in use**

If port `7860` is occupied, configure Gradio to use another available port in `rag_app.py`.

---
<img width="1812" height="1015" alt="image" src="https://github.com/user-attachments/assets/fa36663c-115d-4c47-957a-b8bd5215c8fc" />


*Built with Python, LangChain, Google Gemini, ChromaDB, PyPDF, and Gradio.*
