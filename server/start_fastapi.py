"""Start the FastAPI application with Uvicorn from any working directory."""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parents[1]


def main():
    print("FastAPI: http://127.0.0.1:8000", flush=True)
    print("API docs: http://127.0.0.1:8000/docs", flush=True)
    print("Start MLflow before starting the API.", flush=True)

    return subprocess.call(
        [
            sys.executable,
            "-m", "uvicorn", "App.main:app",
            "--host", "127.0.0.1",
            "--port", "8000",
            "--reload",
            "--reload-dir", str(PROJECT_ROOT / "App"),
        ],
        cwd=PROJECT_ROOT,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
