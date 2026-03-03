from django.db import models

class City(models.Model):
    """Город/населенный пункт"""
    city_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100, verbose_name="Название города")
    region = models.CharField(max_length=100, blank=True, verbose_name="Регион/область")
    lat = models.FloatField(verbose_name="Широта")  
    lon = models.FloatField(verbose_name="Долгота")  
    
    class Meta:
        db_table = 'city'
    
    def __str__(self):
        return f"{self.name}, {self.region}"
    
    def to_android_json(self):
        """Преобразование в формат Android"""
        return {
            'city_ID': self.city_ID,
            'name': self.name,
            'lat': self.lat,
            'lon': self.lon,
            'region': self.region
        }



class WeatherData(models.Model):
    """Данные о погоде (текущие и прогноз)"""
    weather_data_ID = models.AutoField(primary_key=True) 
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
        
    def __str__(self):
        return f"{self.city.name} - {self.date}: {self.temperature}°C"