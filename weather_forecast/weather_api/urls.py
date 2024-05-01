from django.urls import path
from weather_api.views import WeatherAPIView

app_name = "weather_api"

urlpatterns = [
    path('', WeatherAPIView.as_view(), name='weather_api')
]