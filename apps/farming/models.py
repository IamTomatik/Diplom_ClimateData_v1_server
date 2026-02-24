from django.db import models
from apps.users.models import User


class Crop(models.Model):
    """Культура"""
    crop_ID = models.AutoField(primary_key=True)  # добавить
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    imageUri = models.ImageField(upload_to='crops/', null=True, blank=True)  # переименовать photo → imageUri
    
    class Meta:
        db_table = 'crop'
    
    def __str__(self):
        return self.name


class Variety(models.Model):
    """Сорт"""
    variety_ID = models.AutoField(primary_key=True)  # добавить
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='varieties')
    
    name = models.CharField(max_length=200)
    imageUri = models.ImageField(upload_to='varieties/', null=True, blank=True)  # photo → imageUri
    
    # Климатические параметры (имена как в Android)
    optimal_temp_min = models.FloatField()
    optimal_temp_max = models.FloatField()
    optimal_humidity = models.FloatField()
    soil_humidity = models.FloatField()
    growth_days = models.IntegerField()
    
    # Текстовые поля
    risk_factors = models.TextField(blank=True)
    description = models.TextField(blank=True)
    recommended_seedling_time = models.TextField(blank=True)
    recommended_open_ground_time = models.TextField(blank=True)
    recommended_greenhouse_time = models.TextField(blank=True)
    seedling_age = models.TextField(blank=True)
    soil_preparation = models.TextField(blank=True)
    sowing_depth = models.TextField(blank=True)
    planting_scheme = models.TextField(blank=True)
    watering_after_planting = models.TextField(blank=True)
    favorable_conditions = models.TextField(blank=True)
    watering_recommendations = models.TextField(blank=True)
    fertilizing_schedule = models.TextField(blank=True)
    loosening_and_mulching = models.TextField(blank=True)
    disease_prevention = models.TextField(blank=True)
    
    class Meta:
        db_table = 'variety'
    
    def __str__(self):
        return f"{self.crop.name} - {self.name}"

class Location(models.Model):
    """Участок/теплица пользователя"""
    SOIL_TYPES = [
        ('chernozem', 'Чернозем'),
        ('clay', 'Глина'),
        ('sandy', 'Песок'),
        ('loam', 'Суглинок'),
        ('peat', 'Торф'),
        ('podzolic', 'Подзолистая'),
        ('gray_forest', 'Серая лесная'),
        ('chestnut', 'Каштановая'),
        ('saline', 'Засоленная'),
        ('rocky', 'Каменистая'),
    ]
    
    LOCATION_TYPES = [
        ('open_ground', 'Открытый грунт'),
        ('greenhouse', 'Теплица'),
        ('pot', 'Горшок/контейнер'),
        ('raised_bed', 'Высокая грядка'),
        ('hydroponics', 'Гидропоника'),
    ]
    
    locations_ID = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    
    name = models.CharField(max_length=100)
    region = models.CharField(max_length=100)
    area = models.FloatField(null=True, blank=True)
    soil_type = models.CharField(max_length=50, choices=SOIL_TYPES, blank=True)
    description = models.TextField(blank=True)
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES)  # type → location_type
    imageUri = models.ImageField(upload_to='locations/', null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'locations'
    
    def __str__(self):
        return self.name


class Planting(models.Model):
    """Посадка"""
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('harvested', 'Собрано'),
        ('failed', 'Погибло'),
        ('dormant', 'В состоянии покоя'),
    ]
    
    planting_ID = models.AutoField(primary_key=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='plantings')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plantings')
    variety = models.ForeignKey(Variety, on_delete=models.SET_NULL, null=True, blank=True)
    
    name = models.CharField(max_length=100)
    planted_date = models.DateTimeField()
    expected_harvest_date = models.DateTimeField()
    area = models.FloatField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    imageUri = models.ImageField(upload_to='plantings/', null=True, blank=True)  
    
    class Meta:
        db_table = 'planting'
    
    def __str__(self):
        return self.name


class FavoriteCrop(models.Model):
    """Избранные культуры пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorite_crops')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    
    class Meta:
        db_table = 'favorite_crops'
        unique_together = ['user', 'crop']
        verbose_name = 'Избранная культура'
        verbose_name_plural = 'Избранные культуры'


class DiseaseDetection(models.Model):
    """Обнаружение болезней"""
    disease_detection_ID = models.AutoField(primary_key=True)
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, related_name='diseases')
    
    image_path = models.ImageField(upload_to='diseases/')  
    detected_disease = models.CharField(max_length=200)
    confidence = models.FloatField()
    detection_date = models.DateTimeField(auto_now_add=True)
    recommended_action = models.TextField()
    
    class Meta:
        db_table = 'disease_detection'


class Recommendation(models.Model):
    """Рекомендации"""
    PRIORITY_CHOICES = [
        ('high', 'Высокий'),
        ('medium', 'Средний'),
        ('low', 'Низкий'),
    ]

    TYPE_CHOICES = [
        ('watering', 'Полив'),
        ('fertilizing', 'Удобрение'),
        ('harvest', 'Сбор урожая'),
        ('disease', 'Болезнь'),
        ('weather', 'Погода'),
        ('planting', 'Посадка'),
        ('care', 'Уход'),
    ]
    
    recommendations_ID = models.AutoField(primary_key=True)  # добавить
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, null=True, blank=True)
    
    type = models.CharField(max_length=50, choices=TYPE_CHOICES)  # recommendation_type → type
    message = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES)
    generated_date = models.DateTimeField(auto_now_add=True)
    is_completed = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'recommendations'
        
class History(models.Model):
    """История действий"""
    hist_ID = models.AutoField(primary_key=True)  # добавить
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    planting = models.ForeignKey(Planting, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    
    message = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    date = models.DateField(auto_now_add=True)
    
    class Meta:
        db_table = 'history'