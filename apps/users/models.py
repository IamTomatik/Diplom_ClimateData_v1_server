from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь системы"""
    # Убираем phone - его нет в Android
    # phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    
    photo = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="Фото")
    role = models.CharField(max_length=20, default='user', verbose_name="Роль")
    
    # Связь с городом
    city = models.ForeignKey('climate.City', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        db_table = 'users'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
    
    def __str__(self):
        return self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
    
    # Добавим метод для соответствия Android модели
    def to_android_json(self):
        """Преобразование в формат Android приложения"""
        return {
            'user_ID': self.id,
            'email': self.email,
            'name': self.username,  
            'role': self.role,
            'city_id': self.city.id if self.city else None,
            'photo_uri': self.photo.url if self.photo else None,
            # password не передаем!
        }