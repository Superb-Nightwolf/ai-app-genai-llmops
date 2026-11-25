import mlflow
from time import sleep

@mlflow.trace
def generate_answer(question: str):
    sleep(1)
    return f"Answer generated for: {question}"


@mlflow.trace
def process_request(question: str):
    answer = generate_answer(question)
    return answer


if __name__ == "__main__":
    # Run this manual smoke test with the local MLflow server running.
    mlflow.set_tracking_uri("http://127.0.0.1:5000")
    mlflow.set_experiment("agentic-ai-llmops")
    print(process_request("What is RAG?"))
