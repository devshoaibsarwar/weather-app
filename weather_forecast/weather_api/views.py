import json
from datetime import datetime

from django.conf import settings
from django.http import JsonResponse
from django.views.generic import FormView
from django.template.loader import render_to_string

from weather_api.forms import WeatherForm
from weather_api.openweather import OpenWeatherClient
from weather_api.serializers import WeatherSerializer

class WeatherAPIView(FormView):
    form_class = WeatherForm
    template_name = "weather.html"

    def __init__(self, *args, **kwargs):
        self.valid = True
        self.default_forecast_type = "current"
        self.default_location = {
            "latitude": 31.5204,
            "longitude": 74.3587
        }
        self.cache_time = settings.INDEXDB_CACHE_TIME
        self.db_name=settings.INDEXDB_NAME
        self.weather_client = OpenWeatherClient()

        super().__init__(*args, **kwargs)

    def handle_current_weather(self, response, forecast_type):
        weather_data = []
        if response.get("status") == 200:
            serializer = WeatherSerializer(data=response.get("data", {}))
            if serializer.is_valid():
                serialized_data = serializer.data
                html_content = render_to_string("partials/weather_card.html", {
                    "forecast_type": forecast_type,
                    "weather_data": serialized_data
                })
                serialized_data["html"] = html_content
                serialized_data["forecast_type"] = forecast_type
                weather_data.append(serialized_data)

        return weather_data

    def handle_forecast_weather(self, response, forecast_type):
        weather_data = []
        if response.get("status") == 200:
            serializer = WeatherSerializer(data=response.get("data", {}).get("list", []), many=True)
            if serializer.is_valid():
                serialized_data = serializer.data
                for index, forecast in enumerate(serialized_data):
                    forecast["forecast_type"] = forecast_type
                    forecast["lon"] = response.get("data", {}).get("city", {}).get("coord", {}).get("lon")
                    forecast["lat"] = response.get("data", {}).get("city", {}).get("coord", {}).get("lat")
                    html_content = render_to_string("partials/weather_card.html", {
                        "forecast_type": forecast_type,
                        "weather_data": forecast,
                        "card_number": index,
                        "total_cards": len(serialized_data)
                    })
                    forecast["html"] = html_content
                    weather_data.append(forecast)

        return weather_data

    def post(self, request):
        form = WeatherForm(json.loads(request.body))
        if not form.is_valid():
            self.valid = False
            return JsonResponse({
                "status": "ERROR",
                "errors": form.errors
            }, status=400)
        
        forecast_type = form.cleaned_data.get("forecast_type")
        if forecast_type == "current":
            response = self.weather_client.get_current_weather(form.cleaned_data)
            weather_data = self.handle_current_weather(response, forecast_type)

        elif forecast_type == "3-hourly":
            response = self.weather_client.get_weather_forecast(form.cleaned_data)
            weather_data = self.handle_forecast_weather(response, forecast_type)

        if weather_data:
            return JsonResponse({
                "status": "SUCCESS",
                "data": weather_data
            }, status=200)

        return JsonResponse({
            "status": "ERROR",
            "errors": {
                "__all__": response.get("error", "Internal Server Error")
            }
        }, status=400)
        


    def get(self, request):
        response = self.weather_client.get_current_weather(self.default_location)
        weather_data = self.handle_current_weather(response, self.default_forecast_type)

        return self.render_to_response(
            self.get_context_data(
                db_name=self.db_name,
                cache_time=self.cache_time,
                weather_data=weather_data[0] if weather_data else {},
                errors=response.get("error"),
                forecast_type=self.default_forecast_type,
            )
        )
