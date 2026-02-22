from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь системы"""
    phone = models.CharField(max_length=15, blank=True, verbose_name="Телефон")
    photo = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="Фото")
    role = models.CharField(max_length=20, default='user', verbose_name="Роль")  # 'user' или 'admin'
    
    # Связь с городом (из climate)
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