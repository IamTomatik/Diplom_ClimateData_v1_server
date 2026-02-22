from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для модели пользователя"""
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'phone', 'role', 'city', 'photo']
        read_only_fields = ['id', 'role']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'city']
        # username = то что в Android называется 'name'
    
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
            city=validated_data.get('city')
        )
        return user

class LoginSerializer(serializers.Serializer):
    """Сериализатор для входа"""
    username = serializers.CharField(required=True)
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})
    
    def validate(self, attrs):
        """Проверяем учетные данные"""
        username = attrs.get('username')
        password = attrs.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if not user:
                raise serializers.ValidationError("Неверный логин или пароль")
        else:
            raise serializers.ValidationError("Логин и пароль обязательны")
        
        attrs['user'] = user
        return attrs