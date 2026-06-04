from unittest.mock import patch


def test_health_check(client):
    """
    Test that the health check endpoint returns 200 and the correct status message.
    """
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert "running" in data["message"]


def test_ingest_telemetry_success(client):
    """
    Test that a valid telemetry payload is successfully ingested,
    triggers a 201 response, and schedules the background processing task.
    """
    with patch("middleware.api.routes.async_processing") as mock_async_processing:
        payload = {"circuit_id": "CID-BAR-10023", "utilization_mbps": 95.5}
        response = client.post("/api/v1/telemetry", json=payload)
        assert response.status_code == 201

        data = response.json()
        assert data["status"] == "success"
        assert data["message"] == "Alert ingested successfully"
        assert data["recorded_utilization"] == 95.5

        # Verify that the async background task was scheduled with correct parameters
        mock_async_processing.assert_called_once_with(
            circuit_id="CID-BAR-10023", current_utilization=95.5
        )


def test_ingest_telemetry_invalid_payload(client):
    """
    Test that an invalid payload (e.g. negative utilization) fails validation
    and returns a 422 Unprocessable Entity status.
    """
    payload = {
        "circuit_id": "CID-BAR-10023",
        "utilization_mbps": -5.0,  # Invalid, utilization must be >= 0.0
    }
    response = client.post("/api/v1/telemetry", json=payload)
    assert response.status_code == 422
