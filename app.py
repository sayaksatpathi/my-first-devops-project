"""A tiny Flask web app — the sample service for this DevOps/SRE project.

It is instrumented with Prometheus metrics following the RED method
(Rate, Errors, Duration) so the service can be observed in Prometheus and
visualised in Grafana — the foundation of any SRE workflow.
"""
import os
import random
import time

from flask import Flask, Response, g, jsonify, request
from prometheus_client import (
    CONTENT_TYPE_LATEST,
    Counter,
    Gauge,
    Histogram,
    generate_latest,
)

app = Flask(__name__)

# --- Prometheus metrics (the "golden signals" / RED method) ---------------
# Rate + Errors: total requests, labelled so we can slice by status code.
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests.",
    ["method", "endpoint", "http_status"],
)
# Duration: request latency, bucketed so we can compute p50/p95/p99.
REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency in seconds.",
    ["method", "endpoint"],
)
# Saturation (a bonus signal): requests currently being handled.
IN_PROGRESS = Gauge(
    "http_requests_in_progress",
    "Number of HTTP requests currently in progress.",
    ["method", "endpoint"],
)


@app.before_request
def _start_timer():
    g._start_time = time.perf_counter()
    endpoint = request.endpoint or "unknown"
    IN_PROGRESS.labels(request.method, endpoint).inc()


@app.after_request
def _record_metrics(response):
    endpoint = request.endpoint or "unknown"
    # Don't let the /metrics scrape pollute the app's own request metrics.
    if endpoint != "metrics":
        elapsed = time.perf_counter() - getattr(g, "_start_time", time.perf_counter())
        REQUEST_LATENCY.labels(request.method, endpoint).observe(elapsed)
        REQUEST_COUNT.labels(request.method, endpoint, response.status_code).inc()
    IN_PROGRESS.labels(request.method, endpoint).dec()
    return response


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


@app.get("/work")
def work():
    """Simulated workload with variable latency and an occasional failure.

    Useful for generating interesting data on the dashboards and, later, for
    chaos experiments. Tune per request or via env vars:
      - ?fail_rate=0.1  -> 10% of requests return HTTP 500  (env: WORK_FAIL_RATE)
      - ?max_ms=500     -> latency uniformly random in [0, 500]ms (env: WORK_MAX_MS)
    """
    fail_rate = float(
        request.args.get("fail_rate", os.environ.get("WORK_FAIL_RATE", "0.05"))
    )
    max_ms = int(request.args.get("max_ms", os.environ.get("WORK_MAX_MS", "400")))

    time.sleep(random.uniform(0, max_ms) / 1000.0)

    if random.random() < fail_rate:
        return jsonify(status="error", message="simulated failure"), 500
    return jsonify(status="done", message="work complete")


@app.get("/metrics")
def metrics():
    """Prometheus scrape endpoint."""
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8080"))
    app.run(host="0.0.0.0", port=port)
