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
| `.github/workflows/ci.yml` | CI/CD: runs tests, builds & smoke-tests the image, then publishes it to GHCR |

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
3. **Publish** — on pushes to `main` only, pushes the image to the GitHub
   Container Registry (GHCR), tagged with both the commit SHA and `latest`.

You can watch runs under the **Actions** tab on GitHub.

## Pull the published image

Once a build on `main` finishes, the image is available from GHCR:

```bash
docker pull ghcr.io/sayaksatpathi/my-first-devops-project:latest
docker run -p 8080:8080 ghcr.io/sayaksatpathi/my-first-devops-project:latest
```

The package shows up under the repo's **Packages** section on GitHub. The
first publish may create it as private; make it public from the package
settings if you want anyone to pull it without authenticating.

## Next steps (ideas)

- Deploy the published image to a host (Render, Fly.io, AWS, etc.).
- Add linting (ruff) and type checks (mypy) to the pipeline.
