# Em dashboard/urls.py (CRIE ESTE ARQUIVO)
from django.urls import path
from . import views

urlpatterns = [
    # Deixa a URL raiz ('') apontar para a nossa view
    path('', views.dashboard_view, name='dashboard_home'),
    path('settings/', views.settings_view, name='settings'),
]