# gestor/views/feira.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q

from core.models import Feira
from core.forms import FeiraForm

@login_required
def feira_list(request):
    """Lista de feiras"""
    search = request.GET.get('search', '')
    status_filter = request.GET.get('status', '')

    feiras = Feira.objects.all().order_by('-id')

    if search:
        feiras = feiras.filter(
            Q(nome__icontains=search) |
            Q(local__icontains=search) |
            Q(periodo__icontains=search)
        )

    if status_filter:
        feiras = feiras.filter(status=status_filter)

    # Paginação
    paginator = Paginator(feiras, 15)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Status disponíveis
    status_choices = [
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]

    context = {
        'page_obj': page_obj,
        'search': search,
        'status_filter': status_filter,
        'status_choices': status_choices,
    }
    return render(request, 'gestor/feira_list.html', context)

@login_required
def feira_create(request):
    """Criar feira"""
    if request.method == 'POST':
        form = FeiraForm(request.POST)
        if form.is_valid():
            feira = form.save()
            messages.success(
                request,
                f'Feira "{feira.nome}" criada com sucesso!'
            )
            return redirect('gestor:feira_list')
        else:
            messages.error(
                request,
                'Erro ao criar feira. Verifique os dados informados.'
            )
    else:
        form = FeiraForm()

    context = {
        'form': form,
        'title': 'Nova Feira',
        'is_create': True
    }
    return render(request, 'gestor/feira_form.html', context)

@login_required
def feira_update(request, pk):
    """Editar feira"""
    feira = get_object_or_404(Feira, pk=pk)

    if request.method == 'POST':
        form = FeiraForm(request.POST, instance=feira)
        if form.is_valid():
            feira = form.save()
            messages.success(
                request,
                f'Feira "{feira.nome}" atualizada com sucesso!'
            )
            return redirect('gestor:feira_list')
        else:
            messages.error(
                request,
                'Erro ao atualizar feira. Verifique os dados informados.'
            )
    else:
        form = FeiraForm(instance=feira)

    context = {
        'form': form,
        'title': f'Editar Feira: {feira.nome}',
        'feira': feira,
        'is_create': False
    }
    return render(request, 'gestor/feira_form.html', context)

@login_required
def feira_delete(request, pk):
    """Excluir feira"""
    feira = get_object_or_404(Feira, pk=pk)

    if request.method == 'POST':
        nome = feira.nome
        feira.delete()
        messages.success(
            request,
            f'Feira "{nome}" excluída com sucesso!'
        )
        return redirect('gestor:feira_list')

    context = {
        'feira': feira
    }
    return render(request, 'gestor/feira_delete.html', context)
