"""Integration tests for the Mergington High School API."""

from urllib.parse import quote
from fastapi.testclient import TestClient


def test_get_activities(client: TestClient):
    # Arrange
    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data
    assert "description" in data["Chess Club"]
    assert "participants" in data["Chess Club"]


def test_signup_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "newstudent@mergington.edu"

    # Act
    response = client.post(
        f"/activities/{quote(activity)}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email in activities[activity]["participants"]


def test_signup_duplicate(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "duplicate@mergington.edu"
    client.post(
        f"/activities/{quote(activity)}/signup",
        params={"email": email}
    )

    # Act
    response = client.post(
        f"/activities/{quote(activity)}/signup",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_full(client: TestClient):
    # Arrange
    activity = "Basketball Team"
    activities = client.get("/activities").json()
    max_participants = activities[activity]["max_participants"]
    current_count = len(activities[activity]["participants"])

    for i in range(max_participants - current_count):
        client.post(
            f"/activities/{quote(activity)}/signup",
            params={"email": f"fill{i}@mergington.edu"}
        )

    # Act
    response = client.post(
        f"/activities/{quote(activity)}/signup",
        params={"email": "overflow@mergington.edu"}
    )

    # Assert
    assert response.status_code == 400
    assert "Activity is full" in response.json()["detail"]


def test_unregister_success(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "michael@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity)}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 200
    assert email in response.json()["message"]

    activities = client.get("/activities").json()
    assert email not in activities[activity]["participants"]


def test_unregister_not_registered(client: TestClient):
    # Arrange
    activity = "Chess Club"
    email = "notregistered@mergington.edu"

    # Act
    response = client.delete(
        f"/activities/{quote(activity)}/unregister",
        params={"email": email}
    )

    # Assert
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
