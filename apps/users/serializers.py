from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User

        fields = ['user_ID', 'email', 'name', 'role', 'city_id', 'photo_uri']
        read_only_fields = ['user_ID', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
 
        fields = ['username', 'email', 'password', 'password2', 'city_id']
    
    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError("Пароли не совпадают")
        return data
    
    def create(self, validated_data):
        validated_data.pop('password2')
     
        user = User.objects.create_user(
            username=validated_data['username'], 
            email=validated_data['email'],
            password=validated_data['password'],
            name=validated_data['username'], 
            city_id=validated_data.get('city_id')
        )
        return user

class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""
    email = serializers.CharField(required=False)  
    username = serializers.CharField(required=False)
    password = serializers.CharField(write_only=True, required=True)
    
    def validate(self, attrs):
        password = attrs.get('password')
        
        if 'email' in attrs and attrs['email']:
            user = authenticate(username=attrs['email'], password=password)
        elif 'username' in attrs and attrs['username']:
            user = authenticate(username=attrs['username'], password=password)
        else:
            raise serializers.ValidationError("Email или логин обязательны")
        
        if not user:
            raise serializers.ValidationError("Неверный email или пароль")
        
        attrs['user'] = user
        return attrs