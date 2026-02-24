from rest_framework import serializers
from .models import City, WeatherData

class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['city_ID', 'loc_ID', 'name', 'region', 'lat', 'lon']

class WeatherDataSerializer(serializers.ModelSerializer):
    """Сериализатор для погоды"""
    class Meta:
        model = WeatherData
        fields = '__all__'