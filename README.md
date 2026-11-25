# AI Application

```text
AI Application/
|-- .ai-app/                 # Existing Python virtual environment
|-- App/
|   |-- main.py             # FastAPI endpoints
|   |-- llm/                # Model invocation logic
|   |-- agents/             # Future LangGraph workflows
|   |-- rag/                # Future retrieval and embeddings
|   |-- tools/              # Future agent tools and MCP
|   `-- prompts/            # Future prompt templates
|-- storage/
|   |-- mlflow/
|   |   |-- mlflow.db       # Existing tracking database
|   |   `-- artifacts/      # Existing MLflow artifacts
|   `-- vector_db/          # Future vector database
|-- documents/              # Future RAG documents
|-- tests/
|-- requirements.txt
`-- .gitignore
```

Run these PowerShell commands from the project root. Install dependencies if needed:

```powershell
.\.ai-app\Scripts\python.exe -m pip install -r requirements.txt
```

Start MLflow in one terminal using the relocated database and artifacts:

```powershell
.\.ai-app\Scripts\mlflow.exe server --backend-store-uri "sqlite:///storage/mlflow/mlflow.db" --artifacts-destination "./storage/mlflow/artifacts" --host 127.0.0.1 --port 5000
```

Start the API in another terminal:

```powershell
.\.ai-app\Scripts\python.exe -m uvicorn App.main:app --reload
```

The chat endpoint expects Ollama at `http://127.0.0.1:11434` with the `qwen3:4b` model available. The API connects to MLflow at `http://127.0.0.1:5000`; start MLflow before the API.

Run the existing manual MLflow smoke test with MLflow running:

```powershell
.\.ai-app\Scripts\python.exe tests/test_mlflow.py
```
