# my-first-devops-project

A minimal DevOps starter: a tiny Flask web service wired up with tests, a
Dockerfile, and a GitHub Actions CI/CD pipeline. It's intentionally small so you
can see every moving part of a DevOps workflow end to end.

## What's inside

| File | Purpose |
|------|---------|
| `app.py` | A Flask app with `/` and `/health` endpoints |
| `test_app.py` | Pytest tests for both endpoints |
| `requirements.txt` | Runtime dependency (Flask) |
| `requirements-dev.txt` | Dev/test dependencies (adds pytest) |
| `Dockerfile` | Builds a container image that runs the app |
| `.github/workflows/ci.yml` | CI/CD: runs tests, then builds & smoke-tests the image |

## Run it locally

```bash
# 1. Create a virtual environment and install deps
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements-dev.txt

# 2. Run the tests
pytest -v

# 3. Start the app (http://localhost:8080)
python app.py
```

Then open <http://localhost:8080> and <http://localhost:8080/health>.

## Run it with Docker

```bash
docker build -t my-first-devops-project .
docker run -p 8080:8080 my-first-devops-project
```

## The CI/CD pipeline

On every push or pull request to `main`, GitHub Actions:

1. **Test** — installs dependencies and runs `pytest`.
2. **Docker** — builds the container image and smoke-tests it by hitting
   `/health` inside a running container.

You can watch runs under the **Actions** tab on GitHub.

## Next steps (ideas)

- Add a deploy step to push the image to a registry (GHCR, Docker Hub).
- Deploy to a host (Render, Fly.io, AWS, etc.).
- Add linting (ruff) and type checks (mypy) to the pipeline.
