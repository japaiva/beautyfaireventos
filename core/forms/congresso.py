# core/forms/congresso.py

from django import forms
from core.models import Congresso, Feira

class CongressoForm(forms.ModelForm):
    """Formulário para cadastro de Congressos"""

    class Meta:
        model = Congresso
        fields = [
            'status', 'nome', 'feira', 'Periodo',
            'palestrantes', 'diferencial',
            'ingresso_black_valor', 'ingresso_black_link',
            'ingresso_black_lote', 'ingresso_black_status',
            'ingresso_experience_valor', 'ingresso_experience_link',
            'ingresso_experience_lote', 'ingresso_experience_status',
            'tag_chatwoot', 'chatwoot'
        ]
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'feira': forms.Select(attrs={'class': 'form-select'}),
            'Periodo': forms.TextInput(attrs={'class': 'form-control'}),
            'palestrantes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'diferencial': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'ingresso_black_valor': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_black_link': forms.URLInput(attrs={'class': 'form-control'}),
            'ingresso_black_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_black_status': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_experience_valor': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_experience_link': forms.URLInput(attrs={'class': 'form-control'}),
            'ingresso_experience_lote': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_experience_status': forms.TextInput(attrs={'class': 'form-control'}),
            'tag_chatwoot': forms.TextInput(attrs={'class': 'form-control'}),
            'chatwoot': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'status': 'Status',
            'nome': 'Nome do Congresso',
            'feira': 'Feira',
            'Periodo': 'Período',
            'palestrantes': 'Palestrantes',
            'diferencial': 'Diferencial',
            'ingresso_black_valor': 'Black - Valor',
            'ingresso_black_link': 'Black - Link',
            'ingresso_black_lote': 'Black - Lote',
            'ingresso_black_status': 'Black - Status',
            'ingresso_experience_valor': 'Experience - Valor',
            'ingresso_experience_link': 'Experience - Link',
            'ingresso_experience_lote': 'Experience - Lote',
            'ingresso_experience_status': 'Experience - Status',
            'tag_chatwoot': 'Tag Chatwoot',
            'chatwoot': 'Chatwoot',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tornar campos obrigatórios
        self.fields['nome'].required = True
        self.fields['status'].required = True

        # Choices do status
        self.fields['status'].choices = [
            ('', '--- Selecione ---'),
            ('draft', 'Rascunho'),
            ('published', 'Publicado'),
            ('archived', 'Arquivado'),
        ]

        # Choices de feira (apenas feiras publicadas)
        feiras = Feira.objects.filter(status='published').order_by('nome')
        feira_choices = [('', '--- Selecione ---')] + [(f.id, f.nome) for f in feiras]
        self.fields['feira'].choices = feira_choices
