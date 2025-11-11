# Em core/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_view, name='home'),
    path('planos/', views.planos_view, name='planos'),

    # --- [ADICIONE ESTA NOVA ROTA] ---
    path('admin-dashboard/', views.admin_dashboard_view, name='admin_dashboard'),
]