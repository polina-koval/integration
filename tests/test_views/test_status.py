import pytest


@pytest.mark.asyncio
async def test_status_get(client):
    resp = await client.get("/status")
    assert resp.status_code == 200, resp.text
    data = resp.json()
    assert data == {"status": "ok"}
