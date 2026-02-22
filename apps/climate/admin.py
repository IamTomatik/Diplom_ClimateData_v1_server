from django.contrib import admin
from .models import City, WeatherData, ClimateNorm

@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'region', 'latitude', 'longitude']
    search_fields = ['name', 'region']
    ordering = ['name']

@admin.register(WeatherData)
class WeatherDataAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'date', 'temperature', 'humidity', 'is_forecast']
    list_filter = ['city', 'is_forecast']
    search_fields = ['city__name']
    ordering = ['-date']

@admin.register(ClimateNorm)
class ClimateNormAdmin(admin.ModelAdmin):
    list_display = ['id', 'city', 'month', 'avg_temperature', 'avg_humidity']
    list_filter = ['city', 'month']
    ordering = ['city', 'month']