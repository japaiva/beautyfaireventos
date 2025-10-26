# gestor/urls.py

from django.urls import path
from . import views

app_name = 'gestor'

urlpatterns = [
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('home/', views.home, name='home'),

    # Usuários
    path('usuarios/', views.usuario_list, name='usuario_list'),
    path('usuarios/criar/', views.usuario_create, name='usuario_create'),
    path('usuarios/<int:pk>/editar/', views.usuario_update, name='usuario_update'),
    path('usuarios/<int:pk>/excluir/', views.usuario_delete, name='usuario_delete'),

    # Feiras
    path('feiras/', views.feira_list, name='feira_list'),
    path('feiras/criar/', views.feira_create, name='feira_create'),
    path('feiras/<int:pk>/editar/', views.feira_update, name='feira_update'),
    path('feiras/<int:pk>/excluir/', views.feira_delete, name='feira_delete'),

    # Congressos
    path('congressos/', views.congresso_list, name='congresso_list'),
    path('congressos/criar/', views.congresso_create, name='congresso_create'),
    path('congressos/<int:pk>/editar/', views.congresso_update, name='congresso_update'),
    path('congressos/<int:pk>/excluir/', views.congresso_delete, name='congresso_delete'),
]