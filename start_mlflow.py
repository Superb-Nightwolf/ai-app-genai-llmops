"""Start the local MLflow server with project-relative persistent storage."""

from pathlib import Path
import subprocess
import sys


PROJECT_ROOT = Path(__file__).resolve().parent
MLFLOW_STORAGE = PROJECT_ROOT / "storage" / "mlflow"
DATABASE_PATH = MLFLOW_STORAGE / "mlflow.db"
ARTIFACTS_PATH = MLFLOW_STORAGE / "artifacts"


def main():
    ARTIFACTS_PATH.mkdir(parents=True, exist_ok=True)
    print(f"MLflow database: {DATABASE_PATH}", flush=True)
    print(f"MLflow artifacts: {ARTIFACTS_PATH}", flush=True)

    return subprocess.call(
        [
            sys.executable,
            "-m", "mlflow", "server",
            "--backend-store-uri", f"sqlite:///{DATABASE_PATH.as_posix()}",
            "--serve-artifacts",
            "--artifacts-destination", str(ARTIFACTS_PATH),
            "--host", "127.0.0.1",
            "--port", "5000",
            "--workers", "1",
        ],
        cwd=PROJECT_ROOT,
    )


if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        sys.exit(130)
