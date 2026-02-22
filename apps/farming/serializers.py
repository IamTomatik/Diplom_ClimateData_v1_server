from rest_framework import serializers
from .models import Crop, Variety, Location, Planting, Recommendation

class CropSerializer(serializers.ModelSerializer):
    """Сериализатор для культур"""
    class Meta:
        model = Crop
        fields = ['id', 'name', 'category', 'photo']

class VarietySerializer(serializers.ModelSerializer):
    """Сериализатор для сортов"""
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    
    class Meta:
        model = Variety
        fields = [
            'id', 'crop', 'crop_name', 'name', 'photo',
            'optimal_temp_min', 'optimal_temp_max', 'optimal_humidity',
            'soil_humidity', 'growth_days', 'description'
        ]

class LocationSerializer(serializers.ModelSerializer):
    """Сериализатор для участков"""
    class Meta:
        model = Location
        fields = [
            'id', 'name', 'region', 'area', 'soil_type',
            'description', 'location_type', 'photo', 'latitude', 'longitude'
        ]
        read_only_fields = ['id']

class PlantingSerializer(serializers.ModelSerializer):
    """Сериализатор для посадок"""
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    variety_name = serializers.CharField(source='variety.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    class Meta:
        model = Planting
        fields = [
            'id', 'name', 'crop', 'crop_name', 'variety', 'variety_name',
            'location', 'location_name', 'planted_date', 'expected_harvest_date',
            'area', 'status', 'photo'
        ]
        read_only_fields = ['id']

class RecommendationSerializer(serializers.ModelSerializer):
    """Сериализатор для рекомендаций"""
    planting_name = serializers.CharField(source='planting.name', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'id', 'recommendation_type', 'message', 'priority',
            'generated_date', 'is_completed', 'planting', 'planting_name'
        ]