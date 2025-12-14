# app/admin.py
from django.contrib import admin
from .models import Manufacturer, Car, Owner, Ownership, ServiceRecord

# Вспомогательный класс для отображения вкладок ManyToMany
class OwnershipInline(admin.TabularInline):
    model = Ownership
    extra = 1
    verbose_name = "Владение"
    verbose_name_plural = "Владения"

# Админка для Производителя
class ManufacturerAdmin(admin.ModelAdmin):
    # Отображаем только 2 из 6 полей
    list_display = ['name', 'country']  # только название и страну
    list_filter = ['country', 'founded_year']  # фильтрация по стране
    search_fields = ['name', 'country']
    ordering = ['name']
    fieldsets = (
        ('Основная информация', {
            'fields': ('name', 'country', 'founded_year')
        }),
        ('Дополнительная информация', {
            'fields': ('headquarters', 'website', 'description'),
            'classes': ('collapse',)
        }),
    )

# Админка для Автомобиля
class CarAdmin(admin.ModelAdmin):
    # Отображаем только 3 из 10 полей
    list_display = ['model_name', 'manufacturer', 'production_year']  # только модель, производителя и год
    list_filter = ['body_type', 'fuel_type', 'manufacturer']  # фильтрация по типу кузова
    search_fields = ['model_name', 'vin_code', 'manufacturer__name']
    ordering = ['model_name']
    
    # Метод для отображения связанного поля
    def manufacturer_country(self, obj):
        return obj.manufacturer.get_country_display()
    manufacturer_country.short_description = 'Страна производителя'

# Админка для Владельца
class OwnerAdmin(admin.ModelAdmin):
    # Отображаем только 3 из 8 полей
    list_display = ['first_name', 'last_name', 'registration_date']  # только имя, фамилию и дату регистрации
    list_filter = ['gender', 'registration_date']  # фильтрация по полу
    search_fields = ['first_name', 'last_name', 'email']
    inlines = [OwnershipInline]
    
    # Метод для отображения количества автомобилей
    def car_count(self, obj):
        return obj.owned_cars.count()
    car_count.short_description = 'Кол-во автомобилей'

# Админка для Владения
class OwnershipAdmin(admin.ModelAdmin):
    # Отображаем только 3 из 7 полей
    list_display = ['owner', 'car', 'purchase_date']  # только владельца, автомобиль и дату покупки
    list_filter = ['is_current_owner', 'purchase_date']  # фильтрация по текущему владельцу
    search_fields = ['owner__first_name', 'owner__last_name', 'car__model_name']
    list_select_related = ['owner', 'car']

# Админка для Сервисной записи
class ServiceRecordAdmin(admin.ModelAdmin):
    # Отображаем только 3 из 7 полей
    list_display = ['car', 'service_type', 'service_date']  # только автомобиль, тип обслуживания и дату
    list_filter = ['service_type', 'service_date']  # фильтрация по типу обслуживания
    search_fields = ['car__model_name', 'service_center', 'description']
    date_hierarchy = 'service_date'
    
    # Метод для отображения производителя автомобиля
    def car_manufacturer(self, obj):
        return obj.car.manufacturer.name
    car_manufacturer.short_description = 'Производитель'

# Регистрация моделей в админке
admin.site.register(Manufacturer, ManufacturerAdmin)
admin.site.register(Car, CarAdmin)
admin.site.register(Owner, OwnerAdmin)
admin.site.register(Ownership, OwnershipAdmin)
admin.site.register(ServiceRecord, ServiceRecordAdmin)