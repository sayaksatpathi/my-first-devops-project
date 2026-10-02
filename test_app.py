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
    assert "devops-project" in data["message"].lower()


def test_health_is_healthy():
    resp = client().get("/health")
    assert resp.status_code == 200
    assert resp.get_json() == {"status": "healthy"}
