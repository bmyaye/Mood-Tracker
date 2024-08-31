import datetime
import pytest
from httpx import AsyncClient
from moodtracker import models

@pytest.mark.asyncio
async def test_create_mood(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "description": "Feeling happy",
        "mood_type": 1,
        "location": "Home",
        "mood_date": "2023-01-01T00:00:00.000000",
        "user_id": token_user1.user_id
    }
    response = await client.post("/moods", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["description"] == payload["description"]
    assert data["mood_type"] == payload["mood_type"]
    assert data["location"] == payload["location"]
    assert data["user_id"] == payload["user_id"]
    assert data["mood_date"] == payload["mood_date"]


@pytest.mark.asyncio
async def test_update_mood(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    payload = {
        "description": "Feeling great",
        "mood_type": 2,
        "location": "Work"
    }
    mood_id = 1  # Replace with the actual mood ID
    response = await client.put(f"/moods/{mood_id}", json=payload, headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert data["description"] == payload["description"]
    assert data["mood_type"] == payload["mood_type"]
    assert data["location"] == payload["location"]
    assert data["id"] == mood_id


@pytest.mark.asyncio
async def test_list_moods(client: AsyncClient, token_user1: models.Token):
    headers = {"Authorization": f"{token_user1.token_type} {token_user1.access_token}"}
    response = await client.get("/moods", headers=headers)

    data = response.json()

    assert response.status_code == 200
    assert isinstance(data["moods"], list)
    assert len(data["moods"]) > 0

    # Check the first mood
    mood = data["moods"][0]
    assert "description" in mood
    assert "mood_type" in mood
    assert "location" in mood
    assert "mood_date" in mood
    assert "user_id" in mood
