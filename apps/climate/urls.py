from django.urls import path
from . import views
from .views import NearestCityAPIView

urlpatterns = [
    # Города
    path('cities/', views.CityListView.as_view(), name='city-list'),
    path('cities/<int:pk>/', views.CityDetailView.as_view(), name='city-detail'),
    path('cities/by-name/<str:name>/', views.get_city_by_name, name='city-by-name'),
    path('cities/search/', views.SearchCitiesView.as_view(), name='city-search'),
    path('nearest-city/', views.NearestCityAPIView.as_view(), name='nearest-city'),
    
    # Погода
    path('weather/', views.WeatherDataListView.as_view(), name='weather-list'),
    path('nearest_city/', NearestCityAPIView.as_view(), name='nearest_city'),
]