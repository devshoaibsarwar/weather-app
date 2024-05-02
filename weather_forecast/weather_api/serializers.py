from rest_framework import serializers
from datetime import datetime


class CoordSerializer(serializers.Serializer):
    lon = serializers.FloatField()
    lat = serializers.FloatField()


class WeatherItemSerializer(serializers.Serializer):
    description = serializers.CharField()
    icon = serializers.CharField()


class MainSerializer(serializers.Serializer):
    temp = serializers.FloatField()
    feels_like = serializers.FloatField()
    pressure = serializers.IntegerField()
    humidity = serializers.IntegerField()


class WindSerializer(serializers.Serializer):
    speed = serializers.FloatField()
    gust = serializers.FloatField(required=False)


class CloudsSerializer(serializers.Serializer):
    all = serializers.IntegerField()


class CitySerializer(serializers.Serializer):
    coord = CoordSerializer()


class WeatherSerializer(serializers.Serializer):
    main = MainSerializer()
    wind = WindSerializer()
    clouds = CloudsSerializer()
    dt = serializers.IntegerField()
    visibility = serializers.IntegerField()
    weather = WeatherItemSerializer(many=True)
    coord = CoordSerializer(required=False)

        
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        timestamp = representation['dt']    
        forecast_date = datetime.fromtimestamp(timestamp).strftime('%d-%m-%y')
        forecast_time = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S')

        serialized_data = {
            "forecast_date": forecast_date,
            "forecast_time": forecast_time,
            "temprature": representation.get("main", {}).get("temp"),
            "feels_like": representation.get("main", {}).get("feels_like"),
            "pressure": representation.get("main", {}).get("pressure"),
            "visibility": representation.get("visibility") / 1000,
            "humidity": representation.get("main", {}).get("humidity"),
            "wind_speed": round(representation.get("wind", {}).get("speed") * 1.6, 2),
            "clouds": representation.get("clouds", {}).get("all"),
            "weather": {
                "description": representation.get("weather", [{}])[0].get("description"),
                "icon": representation.get("weather", [{}])[0].get("icon"),
            }
        }

        if 'gust' in representation.get('wind'):
            serialized_data["wind_gust"] = round(representation.get('wind').get('gust') * 1.6, 2)

        if representation.get('coord') and 'lon' in representation.get('coord'):
            serialized_data["lon"] = representation.get("coord", {}).get("lon")
            
        if representation.get('coord') and 'lat' in representation.get('coord'):
            serialized_data["lat"] = representation.get("coord", {}).get("lat")


        return serialized_data
