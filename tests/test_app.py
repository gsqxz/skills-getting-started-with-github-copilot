def test_get_activities_returns_all_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "participants" in data["Chess Club"]


def test_signup_success(client, valid_activity_name, test_email):
    response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": test_email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Signed up {test_email} for {valid_activity_name}"
    }

    activities_response = client.get("/activities")
    participants = activities_response.json()[valid_activity_name]["participants"]
    assert test_email in participants


def test_signup_fails_when_activity_not_found(client, invalid_activity_name, test_email):
    response = client.post(
        f"/activities/{invalid_activity_name}/signup",
        params={"email": test_email},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_signup_fails_when_email_already_registered(client, valid_activity_name):
    existing_email = "michael@mergington.edu"

    response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": existing_email},
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Student already signed up for this activity"
    }


def test_unregister_success(client, valid_activity_name, test_email):
    signup_response = client.post(
        f"/activities/{valid_activity_name}/signup",
        params={"email": test_email},
    )
    assert signup_response.status_code == 200

    response = client.delete(
        f"/activities/{valid_activity_name}/signup",
        params={"email": test_email},
    )

    assert response.status_code == 200
    assert response.json() == {
        "message": f"Unregistered {test_email} from {valid_activity_name}"
    }


def test_unregister_fails_when_activity_not_found(client, invalid_activity_name, test_email):
    response = client.delete(
        f"/activities/{invalid_activity_name}/signup",
        params={"email": test_email},
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Activity not found"}


def test_unregister_fails_when_email_is_not_registered(client, valid_activity_name):
    not_registered_email = "not.registered@mergington.edu"

    response = client.delete(
        f"/activities/{valid_activity_name}/signup",
        params={"email": not_registered_email},
    )

    assert response.status_code == 404
    assert response.json() == {
        "detail": "Student is not signed up for this activity"
    }
