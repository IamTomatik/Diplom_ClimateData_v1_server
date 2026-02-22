from rest_framework import serializers
from .models import City, WeatherData

class CitySerializer(serializers.ModelSerializer):
    """Сериализатор для городов"""
    class Meta:
        model = City
        fields = ['id', 'name', 'region', 'latitude', 'longitude']

class WeatherDataSerializer(serializers.ModelSerializer):
    """Сериализатор для погоды"""
    city_name = serializers.CharField(source='city.name', read_only=True)
    
    class Meta:
        model = WeatherData
        fields = [
            'id', 'city', 'city_name', 'date', 'temperature',
            'humidity', 'precipitation', 'wind_speed', 'pressure'
        ]