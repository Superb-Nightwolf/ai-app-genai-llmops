"""Run the application's Qwen model through the local Ollama service."""

import os
from pathlib import Path
import shutil
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]
MODEL = "qwen3:4b"


def main():
    ollama = shutil.which("ollama")
    if ollama is None:
        print("Ollama was not found. Install Ollama and reopen your terminal.", file=sys.stderr)
        return 1

    environment = os.environ.copy()
    environment["OLLAMA_HOST"] = "127.0.0.1:11434"
    print(f"Starting Ollama model: {MODEL}", flush=True)
    print("Ollama API: http://127.0.0.1:11434", flush=True)
    print("Keep the Ollama app/service running for API requests.", flush=True)

    return subprocess.call(
        [ollama, "run", MODEL],
        cwd=PROJECT_ROOT,
        env=environment,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
