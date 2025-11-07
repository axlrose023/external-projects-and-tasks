from fastapi import status


class TestWeatherRoutes:
    def test_get_weather_history_success(self, client, sample_weather_data):
        response = client.get(
            "/weather?day=2024-01-15",
            headers={"x-token": "test-token-32-characters-long-here"},
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["city"] == "TestCity"
        assert data["date"] == "2024-01-15"
        assert len(data["temperatures"]) == 3

        for temp in data["temperatures"]:
            assert "id" in temp
            assert "city" in temp
            assert "temperature" in temp
            assert "date" in temp
            assert "created_at" in temp

    def test_get_weather_history_invalid_token(self, client, sample_weather_data):
        response = client.get(
            "/weather?day=2024-01-15", headers={"x-token": "invalid-token"}
        )

        assert response.status_code == status.HTTP_401_UNAUTHORIZED
        assert response.json()["detail"]["error"] == "Invalid token"

    def test_get_weather_history_missing_token(self, client, sample_weather_data):
        response = client.get("/weather?day=2024-01-15")

        assert response.status_code == status.HTTP_422_UNPROCESSABLE_CONTENT

    def test_get_weather_history_invalid_date_format(self, client, sample_weather_data):
        response = client.get(
            "/weather?day=invalid-date",
            headers={"x-token": "test-token-32-characters-long-here"},
        )

        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert "Invalid date format" in response.json()["detail"]["error"]

    def test_get_weather_history_no_data(self, client):
        response = client.get(
            "/weather?day=2024-01-16",
            headers={"x-token": "test-token-32-characters-long-here"},
        )

        assert response.status_code == status.HTTP_200_OK

        data = response.json()
        assert data["city"] == "TestCity"
        assert data["date"] == "2024-01-16"
        assert data["temperatures"] == []
