import json
import requests
from django.conf import settings
from django.utils.http import urlencode
from requests.exceptions import RequestException 

class OpenWeatherClient:
    def __init__(self):
        self.base_url = settings.OPENWEATHER_BASE_URL
        self.api_key = settings.OPENWEATHER_API_KEY

    def get_current_weather(self, data=None):
        if data is None:
            data = {}
        return self._request('GET', 'weather', data)

    def get_weather_forecast(self, data=None):
        if data is None:
            data = {}
        return self._request('GET', 'forecast', data)

    def _request(self, method, path, data=None):
        params = urlencode({
            'lat': data.get('latitude', ''),
            'lon': data.get('longitude', ''),
            'units': 'metric',
            'appid': self.api_key
        })
        url = f"{self.base_url}/{path}?{params}"
        try:
            response = requests.request(method, url)
            response.raise_for_status()
            
            content_type = response.headers.get('content-type')
            if 'application/json' in content_type:
                response_data = response.json()
            else:
                response_data = response.text

            return {
                'status': response.status_code, 
                'data': response_data
            }
            
        except RequestException as exc:
            if hasattr(exc, 'response') and exc.response is not None:
                content_type = exc.response.headers.get('content-type')
                if 'application/json' in content_type:
                    error_message = exc.response.json().get(
                        "error", 
                        f"Error while requesting OpenWeather API: {exc.response.reason}"
                    )
                else:
                    error_message = f"Error while requesting OpenWeather API: {exc.response.reason}"
                status_code = exc.response.status_code
            else:
                error_message = "Unable to connect to the OpenWeather api."
                status_code = 503  # Service Unavailable

            return {
                'status': status_code, 
                'error': error_message
            }

        