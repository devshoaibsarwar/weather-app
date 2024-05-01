import pytest
from unittest.mock import patch
from rest_framework import status as http_status
from weather_api.views import WeatherAPIView

@pytest.fixture
def weather_api_view():
    return WeatherAPIView()

def test_handle_current_weather(weather_api_view):
    mock_current_weather_response = {
        'status': http_status.HTTP_200_OK,
        'data':  {
            'coord': {
                'lon': -94.04, 
                'lat': 33.4
            }, 
            'weather': [
                {'id': 800, 
                'main': 'Clear', 
                'description': 'clear sky', 
                'icon': '01n'}
            ], 
            'base': 'stations', 
            'main': {
                'temp': 19.93, 
                'feels_like': 20.17, 
                'temp_min': 18.21, 
                'temp_max': 21.08, 
                'pressure': 1011, 
                'humidity': 84
            }, 
            'visibility': 10000, 
            'wind': {
                'speed': 2.68, 
                'deg': 178, 
                'gust': 6.26
            }, 
            'clouds': {
                'all': 0
            }, 
            'dt': 1714554392, 
        }
    }

    weather_data = weather_api_view.handle_current_weather(mock_current_weather_response, "current")
    assert weather_data == [
        {
            "forecast_date": "01-05-24",
            "forecast_time": "09:06:32",
            "temprature": 19.93,
            "feels_like": 20.17,
            "pressure": 1011,
            "visibility": 10,
            "humidity": 84,
            "wind_speed": 4.29,
            "clouds": 0,
            "weather": {
            "description": "clear sky",
            "icon": "01n"
            },
            "wind_gust": 10.02,
            "lon": -94.04,
            "lat": 33.4,
            "html": "\n    <div class=\"card\">\n        \n        <div class=\"card-body\"> \n            <h5 class=\"card-title\">Current Weather</h5>\n            <div class=\"row col-md-10 col-sm-12\">\n                <div class=\"col-sm-5 forecast-image\">\n                    \n                    <img src=\"https://openweathermap.org/img/wn/01n@2x.png\" />\n                    \n                </div>\n                <div class=\"col-sm-6\">\n                    <h6>Temperature</h6>\n                    \n                    <p id=\"temprature\">19.93°C</p>\n                    \n                    <h6>Real Feel</h6>\n                    \n                    <p>20.17°C</p>\n                    \n                </div>\n                </div>\n                <div class=\"row\">\n                    <div class=\"col-sm-6\">\n                        <p class=\"card-text\">Date: 01-05-24</p>\n                        <p class=\"card-text\">Time: 09:06:32</p>\n                        \n                        <p class=\"card-text\">Conditions: Clear Sky</p>\n                        \n                        \n                        <p class=\"card-text\">Wind: 4.29 km/h</p>\n                        \n                        \n                        <p class=\"card-text\">Wind Gusts: 10.02 km/h</p>\n                        \n                        \n                    </div>\n                    <div class=\"col-sm-6\">\n                        \n                        <p class=\"card-text\">Pressure: 1011 mb</p>\n                        \n                        \n                        \n                        <p class=\"card-text\">Humidity: 84%</p>\n                        \n                        \n                        <p class=\"card-text\">Visibility: 10.0 km</p>\n                        \n                    </div>\n                </div>\n        </div>\n    </div>\n",
            "forecast_type": "current"
        }
    ]

def test_handle_forecasr_weather(weather_api_view):
    mock_forecast_weather_response = {
        'status': http_status.HTTP_200_OK,
        'data': {
            "cod":"200",
            "message":0,
            "cnt":40,
            "city":{
                "coord": {
                    "lon":-94.04,
                    "lat": 33.4
                }
            },
            "list":[
                {
                    "dt":1714305600,
                    "main":{
                        "temp":16.46,
                        "feels_like":15.02,
                        "pressure":1013,
                        "humidity":33,
                    },
                    "weather":[
                        {
                        "id":800,
                        "main":"Clear",
                        "description":"clear sky",
                        "icon":"01d"
                        }
                    ],
                    "clouds":{
                        "all":3
                    },
                    "wind":{
                        "speed":9.52,
                        "deg":275,
                        "gust":12.38
                    },
                    "visibility":10000,
                    "dt_txt":"2024-04-28 12:00:00"
                },
                {
                    'weather': [
                        {
                            'id': 800, 
                            'main': 'Clear', 
                            'description': 'clear sky', 
                            'icon': '01n'
                        }
                    ], 
                    'main': {
                        'temp': 19.93, 
                        'feels_like': 20.17, 
                        'temp_min': 18.21, 
                        'temp_max': 21.08, 
                        'pressure': 1011, 
                        'humidity': 84
                    }, 
                    'visibility': 10000, 
                    'wind': {
                        'speed': 2.68, 
                        'deg': 178, 
                        'gust': 6.26
                    }, 
                    'clouds': {
                        'all': 0
                    }, 
                    'dt': 1714554392, 
                }
            ]
        }
    }
    weather_data = weather_api_view.handle_forecast_weather(mock_forecast_weather_response, "3-hourly")
    assert weather_data == [
        {
            "forecast_date": "28-04-24",
            "forecast_time": "12:00:00",
            "temprature": 16.46,
            "feels_like": 15.02,
            "pressure": 1013,
            "visibility": 10,
            "humidity": 33,
            "wind_speed": 15.23,
            "clouds": 3,
            "weather": {
            "description": "clear sky",
            "icon": "01d"
            },
            "wind_gust": 19.81,
            "forecast_type": "3-hourly",
            "lon": -94.04,
            "lat": 33.4,
            "html": "\n    <div class=\"card\">\n        \n            <div id=\"pagination-block\" data-total-cards=\"2\" data-current-card=\"0\" class=\"d-flex justify-content-between mt-2 ml-2 mr-2\">\n    <button id=\"card-back-btn\" class=\"pagination-buttons\" onClick=\"handlePagination('back', '33.4000--94.0400-3-hourly')\"  disabled >\n        <span class=\"material-icons\">\n            navigate_before\n        </span>\n    </button>\n    <button id=\"card-next-btn\" class=\"pagination-buttons\" onClick=\"handlePagination('next', '33.4000--94.0400-3-hourly')\" >\n        <span class=\"material-icons\">\n            navigate_next\n        </span>\n    </button>\n</div>\n\n        \n        <div class=\"card-body\"> \n            <h5 class=\"card-title\">3-Hourly Weather</h5>\n            <div class=\"row col-md-10 col-sm-12\">\n                <div class=\"col-sm-5 forecast-image\">\n                    \n                    <img src=\"https://openweathermap.org/img/wn/01d@2x.png\" />\n                    \n                </div>\n                <div class=\"col-sm-6\">\n                    <h6>Temperature</h6>\n                    \n                    <p id=\"temprature\">16.46°C</p>\n                    \n                    <h6>Real Feel</h6>\n                    \n                    <p>15.02°C</p>\n                    \n                </div>\n                </div>\n                <div class=\"row\">\n                    <div class=\"col-sm-6\">\n                        <p class=\"card-text\">Date: 28-04-24</p>\n                        <p class=\"card-text\">Time: 12:00:00</p>\n                        \n                        <p class=\"card-text\">Conditions: Clear Sky</p>\n                        \n                        \n                        <p class=\"card-text\">Wind: 15.23 km/h</p>\n                        \n                        \n                        <p class=\"card-text\">Wind Gusts: 19.81 km/h</p>\n                        \n                        \n                    </div>\n                    <div class=\"col-sm-6\">\n                        \n                        <p class=\"card-text\">Pressure: 1013 mb</p>\n                        \n                        \n                        <p class=\"card-text\">Clouds: 3%</p>\n                        \n                        \n                        <p class=\"card-text\">Humidity: 33%</p>\n                        \n                        \n                        <p class=\"card-text\">Visibility: 10.0 km</p>\n                        \n                    </div>\n                </div>\n        </div>\n    </div>\n"
        },
        {
            "forecast_date": "01-05-24",
            "forecast_time": "09:06:32",
            "temprature": 19.93,
            "feels_like": 20.17,
            "pressure": 1011,
            "visibility": 10,
            "humidity": 84,
            "wind_speed": 4.29,
            "clouds": 0,
            "weather": {
            "description": "clear sky",
            "icon": "01n"
            },
            "wind_gust": 10.02,
            "forecast_type": "3-hourly",
            "lon": -94.04,
            "lat": 33.4,
            "html": "\n    <div class=\"card\">\n        \n            <div id=\"pagination-block\" data-total-cards=\"2\" data-current-card=\"1\" class=\"d-flex justify-content-between mt-2 ml-2 mr-2\">\n    <button id=\"card-back-btn\" class=\"pagination-buttons\" onClick=\"handlePagination('back', '33.4000--94.0400-3-hourly')\" >\n        <span class=\"material-icons\">\n            navigate_before\n        </span>\n    </button>\n    <button id=\"card-next-btn\" class=\"pagination-buttons\" onClick=\"handlePagination('next', '33.4000--94.0400-3-hourly')\" >\n        <span class=\"material-icons\">\n            navigate_next\n        </span>\n    </button>\n</div>\n\n        \n        <div class=\"card-body\"> \n            <h5 class=\"card-title\">3-Hourly Weather</h5>\n            <div class=\"row col-md-10 col-sm-12\">\n                <div class=\"col-sm-5 forecast-image\">\n                    \n                    <img src=\"https://openweathermap.org/img/wn/01n@2x.png\" />\n                    \n                </div>\n                <div class=\"col-sm-6\">\n                    <h6>Temperature</h6>\n                    \n                    <p id=\"temprature\">19.93°C</p>\n                    \n                    <h6>Real Feel</h6>\n                    \n                    <p>20.17°C</p>\n                    \n                </div>\n                </div>\n                <div class=\"row\">\n                    <div class=\"col-sm-6\">\n                        <p class=\"card-text\">Date: 01-05-24</p>\n                        <p class=\"card-text\">Time: 09:06:32</p>\n                        \n                        <p class=\"card-text\">Conditions: Clear Sky</p>\n                        \n                        \n                        <p class=\"card-text\">Wind: 4.29 km/h</p>\n                        \n                        \n                        <p class=\"card-text\">Wind Gusts: 10.02 km/h</p>\n                        \n                        \n                    </div>\n                    <div class=\"col-sm-6\">\n                        \n                        <p class=\"card-text\">Pressure: 1011 mb</p>\n                        \n                        \n                        \n                        <p class=\"card-text\">Humidity: 84%</p>\n                        \n                        \n                        <p class=\"card-text\">Visibility: 10.0 km</p>\n                        \n                    </div>\n                </div>\n        </div>\n    </div>\n"
        }
    ]