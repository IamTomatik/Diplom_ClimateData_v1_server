from django.contrib import admin
from .models import (
    Crop, Variety, Location, Planting,
    FavoriteCrop, DiseaseDetection, Recommendation, History
)

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['crop_ID', 'name', 'category']
    list_filter = ['category']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Variety)
class VarietyAdmin(admin.ModelAdmin):
    list_display = ['variety_ID', 'name', 'crop', 'optimal_temp_min', 'optimal_temp_max', 'growth_days']
    list_filter = ['crop']
    search_fields = ['name', 'crop__name']
    ordering = ['crop', 'name']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('crop', 'name', 'imageUri', 'description')
        }),
        ('Климатические параметры', {
            'fields': ('optimal_temp_min', 'optimal_temp_max', 'optimal_humidity', 'soil_humidity', 'growth_days')
        }),
        ('Сроки посадки', {
            'fields': ('recommended_seedling_time', 'recommended_open_ground_time',
                      'recommended_greenhouse_time', 'seedling_age')
        }),
        ('Агротехника', {
            'fields': ('soil_preparation', 'sowing_depth', 'planting_scheme', 'watering_after_planting')
        }),
        ('Уход', {
            'fields': ('favorable_conditions', 'watering_recommendations', 'fertilizing_schedule',
                      'loosening_and_mulching', 'disease_prevention')
        }),
        ('Риски', {
            'fields': ('risk_factors',)
        }),
    )

@admin.register(Location)
class LocationAdmin(admin.ModelAdmin):
    list_display = ['locations_ID', 'name', 'user', 'region', 'location_type', 'soil_type']
    list_filter = ['location_type', 'soil_type']
    search_fields = ['name', 'user__username', 'region']
    ordering = ['user', 'name']


@admin.register(Planting)
class PlantingAdmin(admin.ModelAdmin):
    list_display = ['planting_ID', 'name', 'user', 'crop', 'variety', 'location', 'planted_date', 'status']
    list_filter = ['status', 'crop']
    search_fields = ['name', 'user__username', 'crop__name']
    ordering = ['-planted_date']
    date_hierarchy = 'planted_date'
    
    fieldsets = (
        ('Основное', {
            'fields': ('user', 'name', 'crop', 'variety', 'location', 'status', 'imageUri')  # photo → imageUri
        }),
        ('Даты', {
            'fields': ('planted_date', 'expected_harvest_date')
        }),
        ('Параметры', {
            'fields': ('area',)
        }),
    )

@admin.register(FavoriteCrop)
class FavoriteCropAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'crop']
    list_filter = ['crop']
    search_fields = ['user__username', 'crop__name']


@admin.register(DiseaseDetection)
class DiseaseDetectionAdmin(admin.ModelAdmin):
    list_display = ['disease_detection_ID', 'planting', 'detected_disease', 'confidence', 'detection_date']
    list_filter = ['detected_disease']
    search_fields = ['planting__name', 'detected_disease']



@admin.register(Recommendation)
class RecommendationAdmin(admin.ModelAdmin):
    list_display = ['recommendations_ID', 'user', 'type', 'priority', 'generated_date', 'is_completed']
    list_filter = ['type', 'priority', 'is_completed']
    search_fields = ['user__username', 'message']
    ordering = ['-generated_date']


@admin.register(History)
class HistoryAdmin(admin.ModelAdmin):
    list_display = ['hist_ID', 'user', 'message', 'timestamp']
    list_filter = ['date']
    search_fields = ['user__username', 'message']
    ordering = ['-timestamp']