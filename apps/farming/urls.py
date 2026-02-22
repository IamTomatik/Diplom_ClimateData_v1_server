from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'crops', views.CropViewSet)
router.register(r'varieties', views.VarietyViewSet)
router.register(r'locations', views.LocationViewSet)
router.register(r'plantings', views.PlantingViewSet)

urlpatterns = [
    path('', include(router.urls)),
]