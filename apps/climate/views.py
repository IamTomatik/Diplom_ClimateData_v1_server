from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import City, WeatherData
from .serializers import CitySerializer, WeatherDataSerializer

class CityListView(generics.ListAPIView):
    """Список всех городов"""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]  # города может видеть кто угодно

class CityDetailView(generics.RetrieveAPIView):
    """Детальная информация о городе"""
    queryset = City.objects.all()
    serializer_class = CitySerializer
    permission_classes = [permissions.AllowAny]

@api_view(['GET'])
def get_city_by_name(request, name):
    """Получить город по названию"""
    try:
        city = City.objects.get(name__iexact=name)
        serializer = CitySerializer(city)
        return Response(serializer.data)
    except City.DoesNotExist:
        return Response({'error': 'City not found'}, status=404)

class WeatherDataListView(generics.ListAPIView):
    """Список погодных данных"""
    serializer_class = WeatherDataSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_queryset(self):
        # Фильтр по локации, если передан параметр
        location_id = self.request.query_params.get('location', None)
        if location_id:
            return WeatherData.objects.filter(location_id=location_id)
        return WeatherData.objects.all()