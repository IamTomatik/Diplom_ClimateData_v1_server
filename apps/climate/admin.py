from django.contrib import admin
from .models import City, WeatherData

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['city_ID', 'name', 'region', 'lat', 'lon']
    search_fields = ['name', 'region']
    ordering = ['name']

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['weather_data_ID', 'city', 'date', 'temperature', 'humidity', 'is_forecast']
    list_filter = ['city', 'is_forecast']
    search_fields = ['city__name']
    ordering = ['-date']