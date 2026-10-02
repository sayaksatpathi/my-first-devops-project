"""A tiny Flask web app — the sample service for this DevOps project."""
import os

from flask import Flask, jsonify

app = Flask(__name__)


@app.get("/")
def index():
    return jsonify(
        message="Hello from my-first-devops-project!",
        status="ok",
    )


@app.get("/health")
def health():
    """Liveness endpoint used by CI and container health checks."""
    return jsonify(status="healthy"), 200


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
