# project/urls.py (или то что у вас называется как проект)
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')),  # должно быть 'app.urls'
]