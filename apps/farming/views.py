from rest_framework import viewsets, permissions
from .models import Crop, Variety, Location, Planting
from .serializers import CropSerializer, VarietySerializer, LocationSerializer, PlantingSerializer

class CropViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр культур (только чтение)"""
    queryset = Crop.objects.all()
    serializer_class = CropSerializer
    permission_classes = [permissions.AllowAny]

class VarietyViewSet(viewsets.ReadOnlyModelViewSet):
    """Просмотр сортов (только чтение)"""
    queryset = Variety.objects.all()
    serializer_class = VarietySerializer
    permission_classes = [permissions.AllowAny]
    
    def get_queryset(self):
        """Фильтр по культуре, если передан параметр crop"""
        queryset = Variety.objects.all()
        crop_id = self.request.query_params.get('crop', None)
        if crop_id:
            queryset = queryset.filter(crop_id=crop_id)
        return queryset

class LocationViewSet(viewsets.ModelViewSet):
    """Участки пользователя"""
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Location.objects.none()

    def get_queryset(self):
        return Location.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class PlantingViewSet(viewsets.ModelViewSet):
    """Посадки пользователя"""
    serializer_class = PlantingSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = Planting.objects.none() 
    
    def get_queryset(self):
        return Planting.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)