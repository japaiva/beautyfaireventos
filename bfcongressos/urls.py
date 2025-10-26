# bfcongressos/urls.py

from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from core.views import home_view, perfil  # Mudança aqui: home_view ao invés de home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', home_view, name='home'),  # Mudança aqui também
    path('login/', auth_views.LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', perfil, name='perfil'),
    path('gestor/', include('gestor.urls', namespace='gestor')),
]