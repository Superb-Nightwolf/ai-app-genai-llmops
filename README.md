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
|-- start_mlflow.py          # MLflow launcher with absolute storage paths
|-- requirements.txt
`-- .gitignore
```

Run these PowerShell commands from the project root. Install dependencies if needed:

```powershell
.\.ai-app\Scripts\python.exe -m pip install -r requirements.txt
```

Start MLflow in one terminal using the relocated database and artifacts:

```powershell
.\.ai-app\Scripts\python.exe start_mlflow.py
```

The launcher resolves both storage paths from its own location, so the database is always `storage/mlflow/mlflow.db` and artifacts are always under `storage/mlflow/artifacts`, even when invoked by absolute path from another working directory. Use this launcher instead of plain `mlflow server`, which uses storage defaults in the current directory.

The API and smoke test continue connecting to `http://127.0.0.1:5000`. They access storage through the MLflow server and do not need filesystem paths. Existing experiment and trace locations use `mlflow-artifacts:/` references, which the server resolves against the configured artifacts directory.

Start the API in another terminal:

```powershell
.\.ai-app\Scripts\python.exe -m uvicorn App.main:app --reload
```

The chat endpoint expects Ollama at `http://127.0.0.1:11434` with the `qwen3:4b` model available. The API connects to MLflow at `http://127.0.0.1:5000`; start MLflow before the API.

Run the existing manual MLflow smoke test with MLflow running:

```powershell
.\.ai-app\Scripts\python.exe tests/test_mlflow.py
```
