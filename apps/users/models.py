from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь системы"""
 
    user_ID = models.AutoField(primary_key=True)  # добавить
    name = models.CharField(max_length=150)  # добавить (дублирует username?)
    
    photo_uri = models.ImageField(upload_to='users/', null=True, blank=True, verbose_name="Фото")  # переименовать
    role = models.CharField(max_length=20, default='user', verbose_name="Роль")
    
    # Связь с городом
    city_id = models.ForeignKey('climate.City', on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Город", db_column='city_id')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата регистрации")
    
    class Meta:
        db_table = 'users'  
        
    
    def __str__(self):
        return self.name or self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
