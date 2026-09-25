from conftest import register_and_login


def test_preferences_are_user_scoped(client):
    first_headers = register_and_login(client, "first@example.com")
    second_headers = register_and_login(client, "second@example.com")

    assert client.put("/user/preferences", json={"theme": "dark"}, headers=first_headers).status_code == 200
    assert client.put("/user/preferences", json={"language": "hi"}, headers=second_headers).status_code == 200
    assert client.put("/user/preferences", json={}, headers=first_headers).status_code == 422


def test_notifications_and_time_endpoints_require_authentication(client):
    assert client.get("/notifications").status_code == 401
    assert client.get("/panchanga").status_code == 401
    headers = register_and_login(client, "calendar@example.com")
    assert client.put("/notifications/festival", json={"is_enabled": False}, headers=headers).status_code == 200
    assert client.get("/panchanga", headers=headers).status_code == 200
    assert client.get("/vedic-time", headers=headers).status_code == 200


def test_panchanga_can_be_calculated_without_an_account(client):
    response = client.get(
        "/panchanga/calculate",
        params={
            "latitude": 40.7128,
            "longitude": -74.006,
            "elevation": 12.5,
            "timezone": "America/New_York",
        },
    )

    assert response.status_code == 200
    assert response.json()["lunar"]["tithi_name"]


def test_public_panchanga_rejects_unknown_timezone(client):
    response = client.get("/panchanga/calculate", params={"timezone": "Not/A_Timezone"})

    assert response.status_code == 422


def test_public_festival_calendar_returns_month_observances(client):
    response = client.get("/festival/calendar", params={"year": 2026, "month": 10})

    assert response.status_code == 200
    assert {festival["name"] for festival in response.json()["festivals"]} >= {
        "Navratri begins",
        "Gandhi Jayanti",
        "Dussehra",
    }