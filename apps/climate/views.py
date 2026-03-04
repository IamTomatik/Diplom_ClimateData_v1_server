from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from .models import City, WeatherData, get_nearest_city, haversine
from .serializers import CitySerializer, WeatherDataSerializer


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