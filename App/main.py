import httpx
from fastapi import FastAPI, HTTPException
from datetime import datetime, timezone
from pydantic import BaseModel, Field
from time import perf_counter
from uuid import uuid4
import logging
import mlflow
from mlflow.entities import SpanType
import json

logging.basicConfig(
    level=logging.INFO,
    format="%(message)s"
)

logger = logging.getLogger("llmops")

mlflow.set_tracking_uri("http://127.0.0.1:5000")

mlflow.set_experiment("agentic-ai-llmops")

app = FastAPI(
    title="AI Application",
    version="0.0.1",
)


@mlflow.trace(name="ollama_inference", span_type=SpanType.LLM)
def invoke_llm(message: str):

    response = httpx.post(
        "http://127.0.0.1:11434/api/chat",
        json={
            "model": "qwen3:4b",
            "messages": [
                {
                    "role": "user",
                    "content": message
                }
            ],
            "stream": False
        },
        timeout=120.0
    )

    response.raise_for_status()

    result = response.json()

    # Get the currently active MLflow span
    span = mlflow.get_current_active_span()

    # Attach model performance information
    if span is not None:
        span.set_attributes({
            "model": "qwen3:4b",
            "input_tokens": result.get("prompt_eval_count", 0),
            "output_tokens": result.get("eval_count", 0),
            "model_duration_ms": result.get("total_duration", 0) / 1_000_000
        })

    return result


@app.get("/")
def home():
    return {
        "message": "Welcome to the AI Application!"
    }

@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "agentic-ai-api",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }

# Define the expected user request
class ChatRequest(BaseModel):
    message: str = Field(min_length=1)
    session_id: str = "default-session"


# Define the response format
class ChatResponse(BaseModel):
    request_id: str
    answer: str
    latency_ms: float

    model: str
    input_tokens: int
    output_tokens: int
    model_duration_ms: float
    tokens_per_second: float




@app.post("/chat", response_model=ChatResponse)
@mlflow.trace(name="chat_request")
def chat(request: ChatRequest):

    start_time = perf_counter()
    request_id = str(uuid4())

    try:

        # Connect our request ID with the MLflow trace
        mlflow.update_current_trace(
            tags={
                "request_id": request_id,
                "session_id": request.session_id
            }
        )

        # Invoke the separately traced LLM function
        result = invoke_llm(request.message)

        answer = result["message"]["content"]

        input_tokens = result.get("prompt_eval_count", 0)
        output_tokens = result.get("eval_count", 0)

        model_duration_ms = (
            result.get("total_duration", 0) / 1_000_000
        )

        eval_duration_seconds = (
            result.get("eval_duration", 0) / 1_000_000_000
        )

        tokens_per_second = (
            round(output_tokens / eval_duration_seconds, 2)
            if eval_duration_seconds > 0
            else 0.0
        )

        latency_ms = round(
            (perf_counter() - start_time) * 1000, 2
        )

        # Structured logging
        logger.info(
            json.dumps({
                "event": "llm_request_completed",
                "request_id": request_id,
                "model": "qwen3:4b",
                "status": "success",
                "latency_ms": latency_ms,
                "input_tokens": input_tokens,
                "output_tokens": output_tokens,
                "tokens_per_second": tokens_per_second
            })
        )

        return ChatResponse(
            request_id=request_id,
            answer=answer,
            latency_ms=latency_ms,
            model="qwen3:4b",
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            model_duration_ms=round(model_duration_ms, 2),
            tokens_per_second=tokens_per_second
        )

    except httpx.HTTPError as error:

        logger.error(
            json.dumps({
                "event": "llm_request_failed",
                "request_id": request_id,
                "status": "failed",
                "error": str(error)
            })
        )

        raise HTTPException(
            status_code=503,
            detail="LLM service unavailable"
        )
