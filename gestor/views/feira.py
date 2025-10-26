# gestor/views/feira.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
import re
from datetime import datetime

from core.models import Feira
from core.forms import FeiraForm

@login_required
def feira_list(request):
    """Lista de feiras"""
    search = request.GET.get('search', '')
    # Filtro padrão: published (se não especificado)
    status_filter = request.GET.get('status', 'published')

    feiras = Feira.objects.all().order_by('-id')

    if search:
        feiras = feiras.filter(
            Q(nome__icontains=search) |
            Q(local__icontains=search) |
            Q(periodo__icontains=search)
        )

    # Aplicar filtro de status (sempre aplica, padrão é 'published')
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

@login_required
def feira_duplicate(request, pk):
    """Duplicar feira para o próximo ano"""
    feira_original = get_object_or_404(Feira, pk=pk)

    # Criar nova feira baseada na original
    nova_feira = Feira()

    # Copiar todos os campos exceto id e datas
    nova_feira.status = 'draft'  # Sempre começa como rascunho

    # Tentar incrementar o ano no nome
    nome_original = feira_original.nome or ''
    ano_atual = datetime.now().year

    # Procurar por anos no nome (ex: "Beauty Fair 2025")
    anos_encontrados = re.findall(r'\b(20\d{2})\b', nome_original)

    if anos_encontrados:
        # Pega o último ano encontrado e incrementa
        ultimo_ano = int(anos_encontrados[-1])
        novo_ano = ultimo_ano + 1
        novo_nome = nome_original.replace(str(ultimo_ano), str(novo_ano))
    else:
        # Se não encontrou ano, adiciona o próximo ano
        novo_nome = f"{nome_original} {ano_atual + 1}"

    nova_feira.nome = novo_nome
    nova_feira.periodo = feira_original.periodo
    nova_feira.publico_alvo = feira_original.publico_alvo
    nova_feira.credenciamento = feira_original.credenciamento
    nova_feira.local = feira_original.local
    nova_feira.diferencial = feira_original.diferencial
    nova_feira.Observacoes = feira_original.Observacoes
    nova_feira.desconto_nivel_1 = feira_original.desconto_nivel_1
    nova_feira.desconto_nivel_2 = feira_original.desconto_nivel_2
    nova_feira.desconto_cupom_1 = feira_original.desconto_cupom_1
    nova_feira.desconto_cupom_2 = feira_original.desconto_cupom_2
    nova_feira.ingresso_black = feira_original.ingresso_black
    nova_feira.ingresso_experience = feira_original.ingresso_experience
    nova_feira.Infraestrutura_e_servicos = feira_original.Infraestrutura_e_servicos
    nova_feira.Oportunidades_de_negocio = feira_original.Oportunidades_de_negocio
    nova_feira.Gatilhos_de_urgencia = feira_original.Gatilhos_de_urgencia
    nova_feira.credenciamento_categorias = feira_original.credenciamento_categorias
    nova_feira.link_expositores = feira_original.link_expositores
    nova_feira.link_embaixadores = feira_original.link_embaixadores

    # Salvar nova feira
    nova_feira.save()

    messages.success(
        request,
        f'Feira "{feira_original.nome}" duplicada com sucesso! Nova feira: "{nova_feira.nome}"'
    )

    # Redirecionar para edição da nova feira
    return redirect('gestor:feira_update', pk=nova_feira.pk)
