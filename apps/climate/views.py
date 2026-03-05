from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import City, WeatherData, get_nearest_city, haversine
from .serializers import CitySerializer, WeatherDataSerializer
from django.conf import settings 

import aiohttp
import asyncio
import logging

class CityListView(generics.ListAPIView):
    """Список всех городов"""
    queryset = City.objects.all().order_by('name')
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

class CityDetailView(generics.RetrieveAPIView):
    """Детальная информация о городе"""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def get_city_by_name(request, name):
    """Получить город по названию"""
    try:
        # Ищем точное совпадение
        city = City.objects.get(name__iexact=name)
        serializer = CitySerializer(city)
        return Response(serializer.data)
    except City.DoesNotExist:
        # Если точного нет, ищем частичное
        cities = City.objects.filter(name__icontains=name)
        if cities.exists():
            serializer = CitySerializer(cities, many=True)
            return Response(serializer.data)
        return Response(
            {'error': 'City not found'}, 
            status=status.HTTP_404_NOT_FOUND
        )

class WeatherDataListView(generics.ListAPIView):
    """Список погодных данных"""
    serializer_class = WeatherDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        queryset = WeatherData.objects.all()
        
        # Фильтр по городу
        city_id = self.request.query_params.get('city', None)
        if city_id:
            queryset = queryset.filter(city_id=city_id)
        
        # Фильтр по дате (последние N дней)
        days = self.request.query_params.get('days', None)
        if days:
            from django.utils import timezone
            from datetime import timedelta
            date_from = timezone.now() - timedelta(days=int(days))
            queryset = queryset.filter(date__gte=date_from)
        
        return queryset.order_by('-date')

class NearestCityAPIView(APIView):
    """Возвращает ближайший город по координатам"""
    
    def get(self, request):
        # Получаем параметры
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        
        # Валидация
        if lat is None or lon is None:
            return Response(
                {"error": "lat and lon parameters are required"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            lat = float(str(lat).replace(',', '.'))
            lon = float(str(lon).replace(',', '.'))
        except ValueError:
            return Response(
                {"error": "Invalid coordinates format"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Проверка диапазона
        if not (-90 <= lat <= 90) or not (-180 <= lon <= 180):
            return Response(
                {"error": "Coordinates out of range"}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Поиск ближайшего города
        nearest_city = get_nearest_city(lat, lon)
        
        if not nearest_city:
            return Response(
                {"error": "No cities found in database"}, 
                status=status.HTTP_404_NOT_FOUND
            )
        
        # Вычисляем расстояние
        distance = haversine(lat, lon, nearest_city.lat, nearest_city.lon)
        
        # Сериализуем ответ
        serializer = CitySerializer(nearest_city)
        response_data = serializer.data
        response_data['distance_km'] = round(distance, 2)
        
        return Response(response_data)

# Добавляем класс для поиска городов (если нужен)
class SearchCitiesView(APIView):
    """Поиск городов по названию (для автодополнения)"""
    
    def get(self, request):
        query = request.query_params.get('q', '')
        
        if len(query) < 2:
            return Response([])
        
        # Поиск по названию или региону
        cities = City.objects.filter(
            Q(name__icontains=query) | Q(region__icontains=query)
        )[:20]  # Лимит 20 результатов
        
        serializer = CitySerializer(cities, many=True)
        return Response(serializer.data)
    
class WeatherByCoordsAPIView(APIView):
    """
    Получает погоду от OpenWeatherMap по координатам
    (ключ хранится на сервере в settings)
    """
    permission_classes = [permissions.IsAuthenticated]  # Только для авторизованных
    
    async def fetch_weather(self, lat, lon):
        """Асинхронный запрос к OpenWeatherMap"""
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': settings.OPENWEATHER_API_KEY, 
            'units': 'metric',
            'lang': 'ru'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()
    
    def get(self, request):
        # Получаем координаты из запроса
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        
        if not lat or not lon:
            return Response(
                {'error': 'lat and lon are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            weather_data = loop.run_until_complete(
                self.fetch_weather(float(lat), float(lon))
            )
            loop.close()
            
            # Форматируем ответ для Android
            formatted_data = {
                'temperature': f"{round(weather_data['main']['temp'])}°",
                'humidity': str(weather_data['main']['humidity']),
                'wind': str(weather_data['wind']['speed']),
                'pressure': str(weather_data['main']['pressure']),
                'precipitation': str(weather_data.get('rain', {}).get('1h', 0)),
                'city_name': weather_data['name'],
                'description': weather_data['weather'][0]['description']
            }
            
            return Response(formatted_data)
            
        except Exception as e:
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
        
class WeatherForPlantingAPIView(APIView):
    """
    Возвращает погоду для локации, связанной с посадкой
    """
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, planting_id):
        try:
            # Импортируем модель Planting (из другого приложения)
            from plantings.models import Planting
            
            # 1. Находим посадку по ID
            planting = Planting.objects.get(
                plan_id=planting_id,
                user=request.user
            )
            
            # 2. Получаем связанную локацию
            location = planting.location  # предполагаем, что есть связь
            
            # 3. Проверяем, есть ли координаты у локации
            if not location.latitude or not location.longitude:
                return Response(
                    {'error': 'Location has no coordinates'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # 4. Запрашиваем погоду для этих координат
            weather_data = self.fetch_weather(
                location.latitude, 
                location.longitude
            )
            
            # 5. Возвращаем отформатированные данные
            return Response(weather_data)
            
        except Planting.DoesNotExist:
            return Response(
                {'error': 'Planting not found'},
                status=status.HTTP_404_NOT_FOUND
            )
    
    def fetch_weather(self, lat, lon):
        """Запрос к OpenWeatherMap"""

class HourlyForecastAPIView(APIView):

    permission_classes = [permissions.IsAuthenticated]
    
    async def fetch_hourly_forecast(self, lat, lon):
        """Асинхронный запрос к OpenWeatherMap"""
        url = "https://api.openweathermap.org/data/2.5/onecall"
        params = {
            'lat': lat,
            'lon': lon,
            'appid': settings.OPENWEATHER_API_KEY,
            'units': 'metric',
            'lang': 'ru',
            'exclude': 'current,minutely,daily,alerts'
        }
        
        async with aiohttp.ClientSession() as session:
            async with session.get(url, params=params) as response:
                return await response.json()
    
    def get(self, request):
        # Только координаты (city_id не нужен, он уже есть в Android)
        lat = request.query_params.get('lat')
        lon = request.query_params.get('lon')
        hours = request.query_params.get('hours', 48)
        
        if not lat or not lon:
            return Response(
                {'error': 'lat and lon are required'}, 
                status=status.HTTP_400_BAD_REQUEST
            )
        
        try:
            # Асинхронный запрос
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            weather_data = loop.run_until_complete(
                self.fetch_hourly_forecast(float(lat), float(lon))
            )
            loop.close()
            
            if 'hourly' not in weather_data:
                return Response(
                    {'error': 'No hourly forecast data available'}, 
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )
            
            # Форматируем только погодные данные
            hourly_data = weather_data['hourly'][:int(hours)]
            formatted_hourly = []
            
            for hour in hourly_data:
                rain = hour.get('rain', {})
                rain_1h = rain.get('1h', 0) if isinstance(rain, dict) else 0
                
                formatted_hourly.append({
                    'dt': hour['dt'],
                    'temperature': f"{round(hour['temp'])}°",
                    'humidity': str(hour['humidity']),
                    'pressure': str(hour['pressure']),
                    'precipitation': str(rain_1h),
                    'pop': str(hour.get('pop', 0)),
                    'description': hour['weather'][0]['description'],
                    'icon': hour['weather'][0]['icon']
                })
            
            # Возвращаем только массив с погодой
            return Response({
                'hourly': formatted_hourly
            })
            
        except Exception as e:
            logging.error(f"Error fetching hourly forecast: {str(e)}")
            return Response(
                {'error': str(e)}, 
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

