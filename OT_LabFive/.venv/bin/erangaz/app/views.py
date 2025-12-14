# app/views.py
from django.shortcuts import render
from django.views.generic import ListView
from .models import Manufacturer, Car, Owner, ServiceRecord, Ownership
from django.db.models import Count, Avg, Max, Min
from django.utils import timezone
from datetime import timedelta

# VIEW ФУНКЦИИ

def home(request):
    context = {
        'total_cars': Car.objects.count(),
        'total_manufacturers': Manufacturer.objects.count(),
        'total_owners': Owner.objects.count(),
        'total_service_records': ServiceRecord.objects.count(),
        'recent_cars': Car.objects.order_by('-production_year')[:5],
        'recent_service': ServiceRecord.objects.order_by('-service_date')[:3],
    }
    return render(request, 'app/home.html', context)

def car_list(request):
    cars = Car.objects.select_related('manufacturer').all()
    context = {
        'cars': cars,
        'total_count': cars.count(),
        'title': 'Все автомобили',
        'body_types': Car.BODY_TYPE_CHOICES,
        'fuel_types': Car.FUEL_TYPE_CHOICES,
    }
    return render(request, 'app/car_list.html', context)

def cars_by_body_type(request, body_type):
    cars = Car.objects.select_related('manufacturer').filter(body_type=body_type)
    body_type_display = dict(Car.BODY_TYPE_CHOICES).get(body_type, body_type)
    
    context = {
        'cars': cars,
        'total_count': cars.count(),
        'title': f'Автомобили типа: {body_type_display}',
        'filter_type': body_type_display,
        'body_types': Car.BODY_TYPE_CHOICES,
    }
    return render(request, 'app/car_list.html', context)

def service_records(request):
    records = ServiceRecord.objects.select_related('car', 'car__manufacturer').all()
    
    context = {
        'records': records,
        'total_count': records.count(),
        'title': 'Все сервисные записи',
        'service_types': ServiceRecord.SERVICE_TYPE_CHOICES,
    }
    return render(request, 'app/service_records.html', context)

def recent_service_records(request):
    thirty_days_ago = timezone.now().date() - timedelta(days=30)
    records = ServiceRecord.objects.select_related('car', 'car__manufacturer').filter(
        service_date__gte=thirty_days_ago
    ).order_by('-service_date')
    
    context = {
        'records': records,
        'total_count': records.count(),
        'title': 'Недавние сервисные записи (последние 30 дней)',
        'filter_info': 'Фильтр: последние 30 дней',
        'service_types': ServiceRecord.SERVICE_TYPE_CHOICES,
    }
    return render(request, 'app/service_records.html', context)

def car_statistics(request):
    manufacturers_stats = Manufacturer.objects.annotate(
        car_count=Count('cars'),
        avg_price=Avg('cars__price'),
        max_horsepower=Max('cars__horsepower')
    )
    
    body_type_stats = Car.objects.values('body_type').annotate(
        count=Count('id'),
        avg_price=Avg('price'),
        avg_horsepower=Avg('horsepower')
    ).order_by('-count')
    
    fuel_stats = Car.objects.values('fuel_type').annotate(
        count=Count('id'),
        avg_price=Avg('price'),
        avg_year=Avg('production_year')
    ).order_by('-count')
    
    most_expensive_cars = Car.objects.select_related('manufacturer').order_by('-price')[:5]
    most_powerful_cars = Car.objects.select_related('manufacturer').order_by('-horsepower')[:5]
    
    context = {
        'manufacturers_stats': manufacturers_stats,
        'body_type_stats': body_type_stats,
        'fuel_stats': fuel_stats,
        'most_expensive_cars': most_expensive_cars,
        'most_powerful_cars': most_powerful_cars,
        'total_cars': Car.objects.count(),
        'avg_car_price': Car.objects.aggregate(avg_price=Avg('price'))['avg_price'] or 0,
        'total_owners': Owner.objects.count(),
    }
    return render(request, 'app/statistics.html', context)

# VIEW КЛАССЫ

class ManufacturerListView(ListView):
    model = Manufacturer
    template_name = 'app/manufacturer_list.html'
    context_object_name = 'manufacturers'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все производители автомобилей'
        context['countries'] = Manufacturer.COUNTRY_CHOICES
        context['total_count'] = self.get_queryset().count()
        return context

class ManufacturerByCountryView(ListView):
    model = Manufacturer
    template_name = 'app/manufacturer_list.html'
    context_object_name = 'manufacturers'
    
    def get_queryset(self):
        country_code = self.kwargs['country']
        return Manufacturer.objects.filter(country=country_code)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        country_code = self.kwargs['country']
        country_name = dict(Manufacturer.COUNTRY_CHOICES).get(country_code, country_code)
        context['title'] = f'Производители из {country_name}'
        context['filter_info'] = f'Фильтр: страна - {country_name}'
        context['countries'] = Manufacturer.COUNTRY_CHOICES
        context['total_count'] = self.get_queryset().count()
        return context

class OwnerListView(ListView):
    model = Owner
    template_name = 'app/owner_list.html'
    context_object_name = 'owners'
    
    def get_queryset(self):
        return Owner.objects.prefetch_related('owned_cars').all()
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все владельцы автомобилей'
        context['total_count'] = self.get_queryset().count()
        return context

class CurrentOwnersView(ListView):
    model = Owner
    template_name = 'app/owner_list.html'
    context_object_name = 'owners'
    
    def get_queryset(self):
        current_ownerships = Ownership.objects.filter(is_current_owner=True)
        owner_ids = current_ownerships.values_list('owner_id', flat=True).distinct()
        return Owner.objects.filter(id__in=owner_ids).prefetch_related('owned_cars')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Текущие владельцы автомобилей'
        context['filter_info'] = 'Фильтр: текущие владельцы'
        context['total_count'] = self.get_queryset().count()
        return context