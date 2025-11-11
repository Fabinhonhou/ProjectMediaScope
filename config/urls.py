# Em config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # O Dashboard (app 'analytics') continua na raiz
    path('', include('analytics.urls')),
    
    # O Login (app 'accounts') agora vive em "accounts/"
    path('accounts/', include('accounts.urls')), # <-- CORRIGIDO
    path('social/', include('social_django.urls', namespace='social')),
    path('', include('core.urls')),
]