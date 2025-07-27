from fastapi.testclient import TestClient


def test_health_check_endpoint(client: TestClient):
    """Integration test for the health check endpoint."""
    # given
    # when
    response = client.get("/health")

    # then
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
