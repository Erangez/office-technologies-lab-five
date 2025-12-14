# app/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('cars/', views.car_list, name='car_list'),
    path('cars/<str:body_type>/', views.cars_by_body_type, name='cars_by_body_type'),
    path('manufacturers/', views.ManufacturerListView.as_view(), name='manufacturer_list'),
    path('manufacturers/<str:country>/', views.ManufacturerByCountryView.as_view(), name='manufacturers_by_country'),
    path('owners/', views.OwnerListView.as_view(), name='owner_list'),
    path('owners/current/', views.CurrentOwnersView.as_view(), name='current_owners'),
    path('service/', views.service_records, name='service_records'),
    path('service/recent/', views.recent_service_records, name='recent_service_records'),
    path('statistics/', views.car_statistics, name='car_statistics'),
]