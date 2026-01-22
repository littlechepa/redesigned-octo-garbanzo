
import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Soccer Club" in data

@pytest.mark.asyncio
async def test_signup_and_unregister():
    test_email = "pytestuser@mergington.edu"
    test_activity = "Soccer Club"
    # Sign up
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert response.status_code == 200
    # Unregister
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/unregister", json={"name": test_email, "activity": test_activity})
    assert response.status_code == 200
    assert "unregistered" in response.json()["message"].lower()

@pytest.mark.asyncio
async def test_signup_duplicate():
    test_email = "lucas@mergington.edu"
    test_activity = "Soccer Club"
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post(f"/activities/{test_activity}/signup?email={test_email}")
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_unregister_not_found():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        response = await ac.post("/unregister", json={"name": "notfound@mergington.edu", "activity": "Soccer Club"})
    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()
