from pathlib import Path
import sys

import pytest
from fastapi.testclient import TestClient

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from app import app, activities


@pytest.fixture(autouse=True)
def reset_activity_state():
    original_participants = {
        activity_name: list(details["participants"])
        for activity_name, details in activities.items()
    }
    yield
    for activity_name, details in activities.items():
        details["participants"] = list(original_participants[activity_name])


def test_unregister_participant_removes_their_signup():
    client = TestClient(app)

    signup_response = client.post(
        "/activities/Chess Club/signup?email=student@mergington.edu"
    )
    assert signup_response.status_code == 200

    unregister_response = client.delete(
        "/activities/Chess Club/participants/student@mergington.edu"
    )
    assert unregister_response.status_code == 200

    activities_response = client.get("/activities")
    assert activities_response.status_code == 200
    assert "student@mergington.edu" not in activities_response.json()["Chess Club"]["participants"]
