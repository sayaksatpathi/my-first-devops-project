"""Tests for the sample Flask app. Run with: pytest"""
import app as flask_app


def client():
    flask_app.app.config.update(TESTING=True)
    return flask_app.app.test_client()


def test_index_returns_ok():
    resp = client().get("/")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "reliability" in data["message"].lower()


def test_health_is_healthy():
    resp = client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "healthy"}


def test_metrics_endpoint_exposes_prometheus_data():
    # Make a request first so there is something to count.
    client().get("/")
    resp = client().get("/metrics")
    assert resp.status_code == 200
    body = resp.get_data(as_text=True)
    # The RED-method metrics should be present in the scrape output.
    assert "http_requests_total" in body
    assert "http_request_duration_seconds" in body


def test_work_can_be_forced_to_succeed():
    resp = client().get("/work?fail_rate=0&max_ms=0")
    assert resp.status_code == 200
    assert resp.get_json()["status"] == "done"


def test_work_can_be_forced_to_fail():
    resp = client().get("/work?fail_rate=1&max_ms=0")
    assert resp.status_code == 500
    assert resp.get_json()["status"] == "error"
