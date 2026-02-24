from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ['user_ID', 'name', 'email', 'role', 'city_id', 'is_staff', 'created_at']
    list_filter = ['role', 'is_staff', 'is_superuser']
    search_fields = ['name', 'email']
    
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Личная информация', {
            'fields': (
                'name', 'email', 'photo_uri', 'city_id',
            )
        }),
        ('Права', {
            'fields': (
                'role', 'is_active', 'is_staff', 'is_superuser',
                'groups', 'user_permissions'
            )
        }),
        ('Даты', {
            'fields': ('last_login', 'date_joined', 'created_at')
        }),
    )
    
   
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'name', 'email', 'password1', 'password2',
                'role', 'city_id'
            ),
        }),
    )
    

    ordering = ['user_ID']