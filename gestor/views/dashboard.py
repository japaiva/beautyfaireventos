# gestor/views/dashboard.py - Dashboard Beauty Fair Congressos

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import logging

from core.models import Usuario, Feira, Congresso

logger = logging.getLogger('bfcongressos')

@login_required
def home(request):
    """Dashboard principal do gestor"""

    # Estatísticas básicas
    total_usuarios = Usuario.objects.filter(is_active=True).count()

    # Contar feiras e congressos (sem filtrar os itens para evitar erro de JSON)
    try:
        total_feiras = Feira.objects.filter(status='published').count()
    except:
        total_feiras = Feira.objects.count()

    try:
        total_congressos = Congresso.objects.filter(status='published').count()
    except:
        total_congressos = Congresso.objects.count()

    # Itens recentes (contar apenas IDs para evitar erro de JSON)
    try:
        feiras_recentes = list(Feira.objects.values('id', 'nome').order_by('-id')[:5])
    except:
        feiras_recentes = []

    try:
        congressos_recentes = list(Congresso.objects.values('id', 'nome').order_by('-id')[:5])
    except:
        congressos_recentes = []

    context = {
        'total_usuarios': total_usuarios,
        'total_feiras': total_feiras,
        'total_congressos': total_congressos,
        'feiras_recentes': feiras_recentes,
        'congressos_recentes': congressos_recentes,
    }

    return render(request, 'gestor/dashboard.html', context)

@login_required
def dashboard(request):
    """Alias para home"""
    return home(request)