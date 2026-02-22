from django.db import models

class City(models.Model):
    """Город/населенный пункт"""
    name = models.CharField(max_length=100, verbose_name="Название города")
    region = models.CharField(max_length=100, blank=True, verbose_name="Регион/область")
    latitude = models.FloatField(verbose_name="Широта")
    longitude = models.FloatField(verbose_name="Долгота")
    
    class Meta:
        db_table = 'city'
        verbose_name = 'Город'
        verbose_name_plural = 'Города'
    
    def __str__(self):
        return f"{self.name}, {self.region}"


class WeatherData(models.Model):
    """Данные о погоде (текущие и прогноз)"""
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='weather_data')
    date = models.DateTimeField(verbose_name="Дата и время")
    temperature = models.FloatField(verbose_name="Температура (°C)")
    humidity = models.FloatField(verbose_name="Влажность (%)")
    precipitation = models.FloatField(verbose_name="Осадки (мм)", default=0)
    wind_speed = models.FloatField(verbose_name="Скорость ветра (м/с)", default=0)
    pressure = models.FloatField(verbose_name="Давление (гПа)", default=0)
    is_forecast = models.BooleanField(default=False, verbose_name="Это прогноз?")
    source = models.CharField(max_length=50, default='api', verbose_name="Источник данных")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Время получения")
    
    class Meta:
        db_table = 'weather_data'
        verbose_name = 'Данные погоды'
        verbose_name_plural = 'Данные погоды'
        ordering = ['-date']
    
    def __str__(self):
        return f"{self.city.name} - {self.date}: {self.temperature}°C"


class ClimateNorm(models.Model):
    """Климатические нормы для региона (для сравнения)"""
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='climate_norms')
    month = models.IntegerField(verbose_name="Месяц (1-12)")
    avg_temperature = models.FloatField(verbose_name="Средняя температура (°C)")
    avg_humidity = models.FloatField(verbose_name="Средняя влажность (%)")
    avg_precipitation = models.FloatField(verbose_name="Средние осадки (мм)")
    
    class Meta:
        db_table = 'climate_norm'
        verbose_name = 'Климатическая норма'
        verbose_name_plural = 'Климатические нормы'
        unique_together = ['city', 'month']
    
    def __str__(self):
        return f"{self.city.name} - месяц {self.month}"