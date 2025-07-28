import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check_endpoint(client: AsyncClient):
    """Integration test for the health check endpoint."""
    # given
    # when
    response = await client.get("/health")

    # then
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
