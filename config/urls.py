# Em config/urls.py
from django.contrib import admin
from django.urls import path, include # Adicione o 'include'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('analytics.urls')), # <-- ADICIONE ESTA LINHA
]