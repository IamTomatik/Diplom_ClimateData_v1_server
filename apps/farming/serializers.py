from rest_framework import serializers
from .models import Crop, Variety, Location, Planting, Recommendation
from apps.climate.models import City

class CropSerializer(serializers.ModelSerializer):
    """Сериализатор для культур"""
    class Meta:
        model = Crop
        fields = ['crop_ID', 'name', 'category', 'imageUri']

class VarietySerializer(serializers.ModelSerializer):
    """Сериализатор для сортов"""
    cropID = serializers.IntegerField(write_only=True)
    crop_name = serializers.CharField(source='crop.name', read_only=True)
    
    class Meta:
        model = Variety
        fields = [
            'variety_ID', 'cropID', 'crop_name', 'name', 'imageUri',
            'optimal_temp_min', 'optimal_temp_max', 'optimal_humidity',
            'soil_humidity', 'growth_days', 'risk_factors', 'description',
            'recommended_seedling_time', 'recommended_open_ground_time',
            'recommended_greenhouse_time', 'seedling_age', 'soil_preparation',
            'sowing_depth', 'planting_scheme', 'watering_after_planting',
            'favorable_conditions', 'watering_recommendations',
            'fertilizing_schedule', 'loosening_and_mulching', 'disease_prevention'
        ]

    def create(self, validated_data):
        crop_id = validated_data.pop('cropID') 
        crop = Crop.objects.get(crop_ID=crop_id) 
        return Variety.objects.create(crop=crop, **validated_data)

    def update(self, instance, validated_data):
        if 'cropID' in validated_data:
            crop_id = validated_data.pop('cropID')
            instance.crop = Crop.objects.get(crop_ID=crop_id)
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance   

class LocationSerializer(serializers.ModelSerializer):
    """Сериализатор для участков"""

    cityID = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    
    class Meta:
        model = Location
        fields = [
            'locations_ID', 'user', 'city', 'cityID',
            'name', 'region', 'area', 'soil_type',
            'description', 'location_type', 'imageUri'
        ]
        read_only_fields = ['locations_ID']
        extra_kwargs = {
            'user': {'read_only': True},  # user берётся из токена
            'city': {'read_only': True},   # city отдаём, но не принимаем
        }
    
    def create(self, validated_data):
        # Извлекаем cityID, если он есть
        city_id = validated_data.pop('cityID', None)
        
        # Получаем город по ID, если передан
        city = None
        if city_id:
            try:
                city = City.objects.get(city_ID=city_id)
            except City.DoesNotExist:
                pass
        
        # Создаём участок
        location = Location.objects.create(
            city=city,
            **validated_data
        )
        return location
    
    def update(self, instance, validated_data):
        # Обновляем город, если передан cityID
        if 'cityID' in validated_data:
            city_id = validated_data.pop('cityID')
            if city_id:
                try:
                    instance.city = City.objects.get(city_ID=city_id)
                except City.DoesNotExist:
                    instance.city = None
            else:
                instance.city = None
        
        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class PlantingSerializer(serializers.ModelSerializer):

    # ---- READ (возвращаем клиенту) ----
    userID = serializers.IntegerField(source='user.id', read_only=True)
    cropID = serializers.IntegerField(source='crop.crop_ID', read_only=True)
    varietyID = serializers.IntegerField(source='variety.variety_ID', read_only=True)
    locID = serializers.IntegerField(source='location.locations_ID', read_only=True)

    crop_name = serializers.CharField(source='crop.name', read_only=True)
    variety_name = serializers.CharField(source='variety.name', read_only=True)
    location_name = serializers.CharField(source='location.name', read_only=True)
    
    isActive = serializers.SerializerMethodField()

    # ---- WRITE (принимаем от клиента) ----
    crop_id = serializers.IntegerField(write_only=True)
    variety_id = serializers.IntegerField(write_only=True, required=False, allow_null=True)
    loc_id = serializers.IntegerField(write_only=True)

    class Meta:
        model = Planting
        fields = [
            'planting_ID',
            'name',

            # ID
            'userID',
            'cropID',
            'varietyID',
            'locID',

            # имена
            'crop_name',
            'variety_name',
            'location_name',

            # write-only
            'crop_id',
            'variety_id',
            'loc_id',

            # остальное
            'planted_date',
            'expected_harvest_date',
            'area',
            'status',
            'imageUri','isActive'
        ]

        read_only_fields = [
            'planting_ID',
            'userID',
            'cropID',
            'varietyID',
            'locID',
            'crop_name',
            'variety_name',
            'location_name'
        ]

    def get_isActive(self, obj):
        return obj.status == 'active'    

    def create(self, validated_data):
        request = self.context['request']
        user = request.user

        crop_id = validated_data.pop('crop_id')
        variety_id = validated_data.pop('variety_id', None)
        loc_id = validated_data.pop('loc_id')

        crop = Crop.objects.get(crop_ID=crop_id)
        location = Location.objects.get(locations_ID=loc_id)
        variety = Variety.objects.get(variety_ID=variety_id) if variety_id else None

        return Planting.objects.create(
            user=user,
            crop=crop,
            variety=variety,
            location=location,
            **validated_data
        )

    def update(self, instance, validated_data):

        if 'crop_id' in validated_data:
            instance.crop = Crop.objects.get(crop_ID=validated_data.pop('crop_id'))

        if 'variety_id' in validated_data:
            variety_id = validated_data.pop('variety_id')
            instance.variety = Variety.objects.get(variety_ID=variety_id) if variety_id else None

        if 'loc_id' in validated_data:
            instance.location = Location.objects.get(
                locations_ID=validated_data.pop('loc_id')
            )

        for attr, value in validated_data.items():
            setattr(instance, attr, value)

        instance.save()
        return instance

class RecommendationSerializer(serializers.ModelSerializer):
    """Сериализатор для рекомендаций"""
    planting_name = serializers.CharField(source='planting.name', read_only=True)
    
    class Meta:
        model = Recommendation
        fields = [
            'recommendations_ID', 'type', 'message', 'priority',
            'generated_date', 'is_completed', 'planting', 'planting_name'
        ]