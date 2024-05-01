import json
import pytest
from unittest.mock import patch
from weather_api.openweather import OpenWeatherClient

@pytest.fixture
def mock_requests():
    with patch("weather_api.openweather.requests.request") as mock_request:
        yield mock_request

@pytest.fixture
def openweather_client():
    return OpenWeatherClient()

def test_get_current_weather_with_correct_parameters(openweather_client, mock_requests):
    data = {"latitude": "33.44", "lonitude": "-33.44"}
    expected_url = f"{openweather_client.base_url}/weather?lat=33.44&lon=&units=metric&appid=test-api-key"
    openweather_client.get_current_weather(data)
    mock_requests.assert_called_once_with("GET", expected_url)

def test_get_weather_forecasr_request_with_correct_parameters(openweather_client, mock_requests):
    data = {"latitude": "33.44", "lonitude": "-33.44"}
    expected_url = f"{openweather_client.base_url}/forecast?lat=33.44&lon=&units=metric&appid=test-api-key"
    openweather_client.get_weather_forecast(data)
    mock_requests.assert_called_once_with("GET", expected_url)

