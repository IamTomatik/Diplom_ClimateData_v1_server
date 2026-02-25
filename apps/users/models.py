from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Пользователь системы"""
    user_ID = models.AutoField(primary_key=True)
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)  # важно! уникальный
    photo_uri = models.ImageField(upload_to='users/', null=True, blank=True)
    role = models.CharField(max_length=20, default='user')
    city_id = models.ForeignKey('climate.City', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email' 
    REQUIRED_FIELDS = ['name']  
    
    class Meta:
        db_table = 'users'  
        
    
    def __str__(self):
        return self.name or self.username
    
    @property
    def is_admin(self):
        return self.role == 'admin' or self.is_superuser
