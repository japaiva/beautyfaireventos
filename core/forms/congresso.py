# core/forms/congresso.py

from django import forms
from core.models import Congresso, Feira

class CongressoForm(forms.ModelForm):
    """Formulário para cadastro de Congressos"""

    STATUS_CHOICES = [
        ('', '--- Selecione ---'),
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]

    STATUS_INGRESSO_CHOICES = [
        ('', '--- Selecione ---'),
        ('disponivel', 'Disponível'),
        ('esgotado', 'Esgotado'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label='Status'
    )

    feira = forms.ChoiceField(
        choices=[('', '--- Selecione ---')],
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=False,
        label='Feira'
    )

    ingresso_black_status = forms.ChoiceField(
        choices=STATUS_INGRESSO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )

    ingresso_experience_status = forms.ChoiceField(
        choices=STATUS_INGRESSO_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Status'
    )

    class Meta:
        model = Congresso
        fields = [
            'status', 'nome', 'feira', 'Periodo',
            'palestrantes', 'diferencial',
            'ingresso_black_valor', 'ingresso_black_link',
            'ingresso_black_lote', 'ingresso_black_status',
            'ingresso_experience_valor', 'ingresso_experience_link',
            'ingresso_experience_lote', 'ingresso_experience_status',
            'chatwoot'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'Periodo': forms.TextInput(attrs={'class': 'form-control'}),
            'palestrantes': forms.Textarea(attrs={'class': 'form-control', 'rows': 7}),
            'diferencial': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'ingresso_black_valor': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_black_link': forms.URLInput(attrs={'class': 'form-control'}),
            'ingresso_black_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_experience_valor': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_experience_link': forms.URLInput(attrs={'class': 'form-control'}),
            'ingresso_experience_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'chatwoot': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome do Congresso',
            'Periodo': 'Período',
            'palestrantes': 'Palestrantes',
            'diferencial': 'Diferencial',
            'ingresso_black_valor': 'Valor',
            'ingresso_black_link': 'Link',
            'ingresso_black_lote': 'Lote',
            'ingresso_experience_valor': 'Valor',
            'ingresso_experience_link': 'Link',
            'ingresso_experience_lote': 'Lote',
            'chatwoot': 'Chatwoot',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tornar campos obrigatórios
        self.fields['nome'].required = True

        # Choices de feira - se congresso arquivado, mostra feiras publicadas e arquivadas
        if self.instance and self.instance.pk and self.instance.status == 'archived':
            feiras = Feira.objects.filter(status__in=['published', 'archived']).order_by('nome')
        else:
            feiras = Feira.objects.filter(status='published').order_by('nome')

        feira_choices = [('', '--- Selecione ---')] + [(f.id, f.nome) for f in feiras]
        self.fields['feira'].choices = feira_choices
