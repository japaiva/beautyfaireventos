# gestor/views/congresso.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from core.models import Congresso, Feira
from core.forms import CongressoForm

@login_required
def congresso_list(request):
    """Lista de congressos"""
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')
    feira_filter = request.GET.get('feira', '')

    congressos = Congresso.objects.all().order_by('-id')

    if search:
        congressos = congressos.filter(
            Q(nome__icontains=search) |
            Q(Periodo__icontains=search)
        )

    if status_filter:
        congressos = congressos.filter(status=status_filter)

    if feira_filter:
        congressos = congressos.filter(feira=feira_filter)

    # Paginação
    paginator = Paginator(congressos, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Status disponíveis
    status_choices = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]

    # Feiras disponíveis
    feiras_disponiveis = Feira.objects.filter(status='published').order_by('nome')

    context = {
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'feira_filter': feira_filter,
        'status_choices': status_choices,
        'feiras_disponiveis': feiras_disponiveis,
    }
    return render(request, 'gestor/congresso_list.html', context)

@login_required
def congresso_create(request):
    """Criar congresso"""
    if request.method == 'POST':
        form = CongressoForm(request.POST)
        if form.is_valid():
            congresso = form.save()
            messages.success(
                request,
                f'Congresso "{congresso.nome}" criado com sucesso!'
            )
            return redirect('gestor:congresso_list')
        else:
            messages.error(
                request,
                'Erro ao criar congresso. Verifique os dados informados.'
            )
    else:
        form = CongressoForm()

    context = {
        'form': form,
        'title': 'Novo Congresso',
        'is_create': True
    }
    return render(request, 'gestor/congresso_form.html', context)

@login_required
def congresso_update(request, pk):
    """Editar congresso"""
    congresso = get_object_or_404(Congresso, pk=pk)

    if request.method == 'POST':
        form = CongressoForm(request.POST, instance=congresso)
        if form.is_valid():
            congresso = form.save()
            messages.success(
                request,
                f'Congresso "{congresso.nome}" atualizado com sucesso!'
            )
            return redirect('gestor:congresso_list')
        else:
            messages.error(
                request,
                'Erro ao atualizar congresso. Verifique os dados informados.'
            )
    else:
        form = CongressoForm(instance=congresso)

    context = {
        'form': form,
        'title': f'Editar Congresso: {congresso.nome}',
        'congresso': congresso,
        'is_create': False
    }
    return render(request, 'gestor/congresso_form.html', context)

@login_required
def congresso_delete(request, pk):
    """Excluir congresso"""
    congresso = get_object_or_404(Congresso, pk=pk)

    if request.method == 'POST':
        nome = congresso.nome
        congresso.delete()
        messages.success(
            request,
            f'Congresso "{nome}" excluído com sucesso!'
        )
        return redirect('gestor:congresso_list')

    context = {
        'congresso': congresso
    }
    return render(request, 'gestor/congresso_delete.html', context)
