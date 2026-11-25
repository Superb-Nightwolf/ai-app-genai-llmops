"""Ollama model invocation and MLflow inference tracing."""

import httpx
import mlflow
from mlflow.entities import SpanType


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
