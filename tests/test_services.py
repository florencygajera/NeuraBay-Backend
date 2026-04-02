import pytest


@pytest.mark.anyio
async def test_services_list(client):
    res = await client.get("/api/v1/services")
    assert res.status_code == 200
    body = res.json()
    assert body["success"] is True
