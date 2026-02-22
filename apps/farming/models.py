from django.db import models
from apps.users.models import User
from apps.climate.models import City

class Crop(models.Model):
    """Культура (томат, огурец, пшеница и т.д.)"""
    name = models.CharField(max_length=100, verbose_name="Название")
    category = models.CharField(max_length=100, verbose_name="Категория")
    photo = models.ImageField(upload_to='crops/', null=True, blank=True, verbose_name="Фото")
    
    class Meta:
        db_table = 'crop'
        verbose_name = 'Культура'
        verbose_name_plural = 'Культуры'
    
    def __str__(self):
        return self.name


class Variety(models.Model):
    """Сорт (эталонные данные от админа)"""
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, related_name='varieties', verbose_name="Культура")
    name = models.CharField(max_length=200, verbose_name="Название сорта")
    photo = models.ImageField(upload_to='varieties/', null=True, blank=True, verbose_name="Фото")
    
    # Климатические параметры
    optimal_temp_min = models.FloatField(verbose_name="Мин. температура (°C)")
    optimal_temp_max = models.FloatField(verbose_name="Макс. температура (°C)")
    optimal_humidity = models.FloatField(verbose_name="Оптимальная влажность воздуха (%)")
    soil_humidity = models.FloatField(verbose_name="Влажность почвы (%)")
    growth_days = models.IntegerField(verbose_name="Дней до созревания")
    
    # Факторы риска и описание
    risk_factors = models.TextField(verbose_name="Факторы риска", blank=True)
    description = models.TextField(verbose_name="Описание", blank=True)
    
    # Сроки посадки
    recommended_seedling_time = models.TextField(verbose_name="Сроки посева на рассаду", blank=True)
    recommended_open_ground_time = models.TextField(verbose_name="Сроки высадки в открытый грунт", blank=True)
    recommended_greenhouse_time = models.TextField(verbose_name="Сроки высадки в теплицу", blank=True)
    seedling_age = models.TextField(verbose_name="Возраст рассады", blank=True)
    
    # Агротехника
    soil_preparation = models.TextField(verbose_name="Подготовка почвы", blank=True)
    sowing_depth = models.TextField(verbose_name="Глубина посева", blank=True)
    planting_scheme = models.TextField(verbose_name="Схема посадки", blank=True)
    watering_after_planting = models.TextField(verbose_name="Полив после посадки", blank=True)
    
    # Уход
    favorable_conditions = models.TextField(verbose_name="Благоприятные условия", blank=True)
    watering_recommendations = models.TextField(verbose_name="Рекомендации по поливу", blank=True)
    fertilizing_schedule = models.TextField(verbose_name="График подкормок", blank=True)
    loosening_and_mulching = models.TextField(verbose_name="Рыхление и мульчирование", blank=True)
    disease_prevention = models.TextField(verbose_name="Профилактика болезней", blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'variety'
        verbose_name = 'Сорт'
        verbose_name_plural = 'Сорта'
    
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    name = models.CharField(max_length=100, verbose_name="Название участка")
    region = models.CharField(max_length=100, verbose_name="Регион/область")
    area = models.FloatField(null=True, blank=True, verbose_name="Площадь (м²)")
    soil_type = models.CharField(max_length=50, choices=SOIL_TYPES, blank=True, verbose_name="Тип почвы")
    description = models.TextField(blank=True, verbose_name="Описание")
    location_type = models.CharField(max_length=50, choices=LOCATION_TYPES, verbose_name="Тип расположения")
    photo = models.ImageField(upload_to='locations/', null=True, blank=True, verbose_name="Фото")
    
    # Координаты
    latitude = models.FloatField(null=True, blank=True, verbose_name="Широта")
    longitude = models.FloatField(null=True, blank=True, verbose_name="Долгота")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'locations'
        verbose_name = 'Участок'
        verbose_name_plural = 'Участки'
    
    def __str__(self):
        return f"{self.name} ({self.user.username})"


class Planting(models.Model):
    """Посадка"""
    STATUS_CHOICES = [
        ('active', 'Активно'),
        ('harvested', 'Собрано'),
        ('failed', 'Погибло'),
        ('dormant', 'В состоянии покоя'),
    ]
    
    location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='plantings', verbose_name="Участок")
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE, verbose_name="Культура")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='plantings', verbose_name="Пользователь")
    variety = models.ForeignKey(Variety, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Сорт")
    
    name = models.CharField(max_length=100, verbose_name="Название посадки")
    planted_date = models.DateTimeField(verbose_name="Дата посадки")
    expected_harvest_date = models.DateTimeField(verbose_name="Ожидаемая дата сбора")
    area = models.FloatField(verbose_name="Площадь посадки (м²)")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active', verbose_name="Статус")
    photo = models.ImageField(upload_to='plantings/', null=True, blank=True, verbose_name="Фото")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата обновления")
    
    class Meta:
        db_table = 'planting'
        verbose_name = 'Посадка'
        verbose_name_plural = 'Посадки'
    
    def __str__(self):
        return f"{self.name} ({self.crop.name})"


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
    """Обнаруженные болезни"""
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, related_name='diseases')
    image = models.ImageField(upload_to='diseases/', verbose_name="Фото")
    detected_disease = models.CharField(max_length=200, verbose_name="Обнаруженная болезнь")
    confidence = models.FloatField(verbose_name="Уверенность (%)")
    detection_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата обнаружения")
    recommended_action = models.TextField(verbose_name="Рекомендуемые действия")
    
    class Meta:
        db_table = 'disease_detection'
        verbose_name = 'Обнаружение болезни'
        verbose_name_plural = 'Обнаружения болезней'


class Recommendation(models.Model):
    """Рекомендации для пользователя"""
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
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recommendations')
    planting = models.ForeignKey(Planting, on_delete=models.CASCADE, null=True, blank=True)
    recommendation_type = models.CharField(max_length=50, choices=TYPE_CHOICES, verbose_name="Тип")
    message = models.TextField(verbose_name="Сообщение")
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, verbose_name="Приоритет")
    generated_date = models.DateTimeField(auto_now_add=True, verbose_name="Дата генерации")
    is_completed = models.BooleanField(default=False, verbose_name="Выполнено")
    
    class Meta:
        db_table = 'recommendations'
        verbose_name = 'Рекомендация'
        verbose_name_plural = 'Рекомендации'
        ordering = ['-generated_date']


class History(models.Model):
    """История действий пользователя"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='history')
    planting = models.ForeignKey(Planting, on_delete=models.SET_NULL, null=True, blank=True)
    location = models.ForeignKey(Location, on_delete=models.SET_NULL, null=True, blank=True)
    message = models.TextField(verbose_name="Сообщение")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="Время")
    date = models.DateField(auto_now_add=True, verbose_name="Дата")
    
    class Meta:
        db_table = 'history'
        verbose_name = 'История'
        verbose_name_plural = 'История действий'
        ordering = ['-timestamp']