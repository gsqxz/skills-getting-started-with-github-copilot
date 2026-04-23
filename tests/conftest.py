from copy import deepcopy

import pytest
from fastapi.testclient import TestClient

from src.app import activities, app


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def valid_activity_name():
    return "Chess Club"


@pytest.fixture
def invalid_activity_name():
    return "Nonexistent Club"


@pytest.fixture
def test_email():
    return "test.student@mergington.edu"


@pytest.fixture(autouse=True)
def reset_activities_state():
    """Keep tests isolated from the global in-memory activities state."""
    original_activities = deepcopy(activities)
    yield
    activities.clear()
    activities.update(original_activities)
