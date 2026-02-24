from django.urls import path
from . import views

urlpatterns = [
    # Города
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', views.CityDetailView.as_view(), name='city-detail'),
    path('cities/by-name/<str:name>/', views.get_city_by_name, name='city-by-name'),
    
    # Погода
    path('weather/', views.WeatherDataListView.as_view(), name='weather-list'),
]