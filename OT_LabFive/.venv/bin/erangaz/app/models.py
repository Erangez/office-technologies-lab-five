# app/models.py
from django.db import models

# Модель 1: Производитель (Manufacturer)
class Manufacturer(models.Model):
    COUNTRY_CHOICES = [
        ('GER', 'Германия'),
        ('JPN', 'Япония'),
        ('USA', 'США'),
        ('KOR', 'Южная Корея'),
        ('FRA', 'Франция'),
        ('ITA', 'Италия'),
        ('UK', 'Великобритания'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Название производителя")
    country = models.CharField(max_length=3, choices=COUNTRY_CHOICES, verbose_name="Страна")
    founded_year = models.IntegerField(verbose_name="Год основания")
    headquarters = models.CharField(max_length=100, verbose_name="Штаб-квартира")
    website = models.URLField(verbose_name="Веб-сайт")
    description = models.TextField(verbose_name="Описание")
    
    class Meta:
        verbose_name = "Производитель"
        verbose_name_plural = "Производители"
        ordering = ['name']  # сортировка по умолчанию
    
    def __str__(self):
        return self.name

# Модель 2: Автомобиль (Car)
class Car(models.Model):
    BODY_TYPE_CHOICES = [
        ('SEDAN', 'Седан'),
        ('HATCHBACK', 'Хэтчбек'),
        ('SUV', 'Внедорожник'),
        ('COUPE', 'Купе'),
        ('CONVERTIBLE', 'Кабриолет'),
        ('WAGON', 'Универсал'),
        ('PICKUP', 'Пикап'),
    ]
    
    FUEL_TYPE_CHOICES = [
        ('PETROL', 'Бензин'),
        ('DIESEL', 'Дизель'),
        ('ELECTRIC', 'Электрический'),
        ('HYBRID', 'Гибрид'),
        ('HYDROGEN', 'Водородный'),
    ]
    
    model_name = models.CharField(max_length=100, verbose_name="Модель")
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, verbose_name="Производитель", related_name="cars")
    production_year = models.IntegerField(verbose_name="Год выпуска")
    body_type = models.CharField(max_length=15, choices=BODY_TYPE_CHOICES, verbose_name="Тип кузова")
    engine_volume = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Объем двигателя (л)")
    horsepower = models.IntegerField(verbose_name="Мощность (л.с.)")
    fuel_type = models.CharField(max_length=10, choices=FUEL_TYPE_CHOICES, verbose_name="Тип топлива")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена ($)")
    color = models.CharField(max_length=30, verbose_name="Цвет")
    vin_code = models.CharField(max_length=17, unique=True, verbose_name="VIN код")
    
    class Meta:
        verbose_name = "Автомобиль"
        verbose_name_plural = "Автомобили"
        ordering = ['-production_year']  # сортировка по умолчанию
    
    def __str__(self):
        return f"{self.manufacturer.name} {self.model_name}"

# Модель 3: Владелец (Owner)
class Owner(models.Model):
    GENDER_CHOICES = [
        ('M', 'Мужской'),
        ('F', 'Женский'),
        ('O', 'Другое'),
    ]
    
    first_name = models.CharField(max_length=50, verbose_name="Имя")
    last_name = models.CharField(max_length=50, verbose_name="Фамилия")
    birth_date = models.DateField(verbose_name="Дата рождения")
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, verbose_name="Пол")
    phone = models.CharField(max_length=15, verbose_name="Телефон")
    email = models.EmailField(verbose_name="Электронная почта")
    registration_date = models.DateField(verbose_name="Дата регистрации")
    owned_cars = models.ManyToManyField(Car, verbose_name="Автомобили во владении", related_name="owners", through='Ownership')
    
    class Meta:
        verbose_name = "Владелец"
        verbose_name_plural = "Владельцы"
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"

# Модель 4: Владение (Ownership) - для связи ManyToMany с дополнительными полями
class Ownership(models.Model):
    owner = models.ForeignKey(Owner, on_delete=models.CASCADE, verbose_name="Владелец")
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль")
    purchase_date = models.DateField(verbose_name="Дата покупки")
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена покупки")
    is_current_owner = models.BooleanField(default=True, verbose_name="Текущий владелец")
    mileage_at_purchase = models.IntegerField(verbose_name="Пробег при покупке (км)")
    
    class Meta:
        verbose_name = "Владение"
        verbose_name_plural = "Владения"
        unique_together = ['owner', 'car']
    
    def __str__(self):
        return f"{self.owner} - {self.car}"

# Модель 5: Сервисное обслуживание (ServiceRecord)
class ServiceRecord(models.Model):
    SERVICE_TYPE_CHOICES = [
        ('OIL_CHANGE', 'Замена масла'),
        ('BRAKE_REPAIR', 'Ремонт тормозов'),
        ('TIRE_CHANGE', 'Замена шин'),
        ('ENGINE_REPAIR', 'Ремонт двигателя'),
        ('TRANSMISSION', 'Ремонт коробки передач'),
        ('ELECTRICAL', 'Электрика'),
        ('BODY_REPAIR', 'Кузовной ремонт'),
        ('MAINTENANCE', 'Техническое обслуживание'),
    ]
    
    car = models.ForeignKey(Car, on_delete=models.CASCADE, verbose_name="Автомобиль", related_name="service_records")
    service_type = models.CharField(max_length=20, choices=SERVICE_TYPE_CHOICES, verbose_name="Тип обслуживания")
    service_date = models.DateField(verbose_name="Дата обслуживания")
    cost = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Стоимость ($)")
    service_center = models.CharField(max_length=100, verbose_name="Сервисный центр")
    description = models.TextField(verbose_name="Описание работ")
    mileage = models.IntegerField(verbose_name="Пробег на момент обслуживания (км)")
    
    class Meta:
        verbose_name = "Запись об обслуживании"
        verbose_name_plural = "Записи об обслуживании"
        ordering = ['-service_date']
    
    def __str__(self):
        return f"{self.car} - {self.service_type} ({self.service_date})"