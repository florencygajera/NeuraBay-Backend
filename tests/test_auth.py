import pytest


@pytest.mark.anyio
async def test_register_and_login(client):
    payload = {"email": "user1@neurabay.com", "full_name": "User One", "password": "Pass1234"}
    res = await client.post("/api/v1/auth/register", json=payload)
    assert res.status_code == 200

    login_data = {"username": "user1@neurabay.com", "password": "Pass1234"}
    res = await client.post("/api/v1/auth/login", data=login_data)
    assert res.status_code == 200
    body = res.json()
    assert "access_token" in body
    assert "refresh_token" in body
