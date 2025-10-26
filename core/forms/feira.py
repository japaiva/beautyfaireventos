# core/forms/feira.py

from django import forms
from core.models import Feira
import json
import ast

class FeiraForm(forms.ModelForm):
    """Formulário para cadastro de Feiras"""

    STATUS_CHOICES = [
        ('', '--- Selecione ---'),
        ('draft', 'Rascunho'),
        ('published', 'Publicado'),
        ('archived', 'Arquivado'),
    ]

    status = forms.ChoiceField(
        choices=STATUS_CHOICES,
        widget=forms.Select(attrs={'class': 'form-select'}),
        required=True,
        label='Status'
    )

    # Campo para editar credenciamento_categorias como JSON (gerenciado via JavaScript)
    credenciamento_categorias = forms.CharField(
        required=False,
        widget=forms.HiddenInput(),
        label='Credenciamento - Categorias'
    )

    class Meta:
        model = Feira
        fields = [
            'status', 'nome', 'periodo', 'publico_alvo', 'credenciamento',
            'local', 'diferencial', 'Observacoes',
            'desconto_nivel_1', 'desconto_nivel_2',
            'desconto_cupom_1', 'desconto_cupom_2',
            'ingresso_black', 'ingresso_experience',
            'Infraestrutura_e_servicos', 'Oportunidades_de_negocio',
            'Gatilhos_de_urgencia', 'link_expositores', 'link_embaixadores',
            'credenciamento_categorias'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'periodo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'publico_alvo': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'credenciamento': forms.Textarea(attrs={'class': 'form-control', 'rows': 5}),
            'local': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'diferencial': forms.Textarea(attrs={'class': 'form-control', 'rows': 2}),
            'Observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'desconto_nivel_1': forms.TextInput(attrs={'class': 'form-control'}),
            'desconto_nivel_2': forms.TextInput(attrs={'class': 'form-control'}),
            'desconto_cupom_1': forms.TextInput(attrs={'class': 'form-control'}),
            'desconto_cupom_2': forms.TextInput(attrs={'class': 'form-control'}),
            'ingresso_black': forms.Textarea(attrs={'class': 'form-control', 'rows': 11}),
            'ingresso_experience': forms.Textarea(attrs={'class': 'form-control', 'rows': 11}),
            'Infraestrutura_e_servicos': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Oportunidades_de_negocio': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'Gatilhos_de_urgencia': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'link_expositores': forms.URLInput(attrs={'class': 'form-control'}),
            'link_embaixadores': forms.URLInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'nome': 'Nome da Feira',
            'periodo': 'Período',
            'publico_alvo': 'Público Alvo',
            'credenciamento': 'Credenciamento',
            'local': 'Local',
            'diferencial': 'Diferencial',
            'Observacoes': 'Observações',
            'desconto_nivel_1': 'Desconto Nível 1',
            'desconto_nivel_2': 'Desconto Nível 2',
            'desconto_cupom_1': 'Desconto Cupom 1',
            'desconto_cupom_2': 'Desconto Cupom 2',
            'ingresso_black': 'Ingresso Black',
            'ingresso_experience': 'Ingresso Experience',
            'Infraestrutura_e_servicos': 'Infraestrutura e Serviços',
            'Oportunidades_de_negocio': 'Oportunidades de Negócio',
            'Gatilhos_de_urgencia': 'Gatilhos de Urgência',
            'link_expositores': 'Link Expositores',
            'link_embaixadores': 'Link Embaixadores',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Tornar campos obrigatórios
        self.fields['nome'].required = True

        # Se está editando, garantir que o JSON seja válido
        if self.instance and self.instance.pk and self.instance.credenciamento_categorias:
            try:
                raw_value = self.instance.credenciamento_categorias

                # Se já é uma lista/dict Python, converte pra JSON
                if isinstance(raw_value, str):
                    # Tentar substituir aspas simples por duplas se for necessário
                    try:
                        data = json.loads(raw_value)
                    except json.JSONDecodeError:
                        # Tentar converter aspas simples para duplas usando ast
                        data = ast.literal_eval(raw_value)
                else:
                    data = raw_value

                # Converter para JSON válido com aspas duplas
                json_valid = json.dumps(data, ensure_ascii=False)
                self.fields['credenciamento_categorias'].initial = json_valid
            except (json.JSONDecodeError, TypeError, ValueError, SyntaxError):
                # Se não conseguir fazer parse, deixa vazio
                self.fields['credenciamento_categorias'].initial = ''

    def clean_credenciamento_categorias(self):
        """Valida e converte o JSON de credenciamento_categorias"""
        data = self.cleaned_data.get('credenciamento_categorias', '')

        if not data or data.strip() == '':
            return None

        try:
            # Tenta fazer parse do JSON
            parsed = json.loads(data)
            # Retorna como string JSON para salvar no banco
            return json.dumps(parsed, ensure_ascii=False)
        except json.JSONDecodeError as e:
            raise forms.ValidationError(f'JSON inválido: {str(e)}')

    def save(self, commit=True):
        """Sobrescreve save para garantir que o JSON seja salvo corretamente"""
        instance = super().save(commit=False)

        # O campo já foi processado pelo clean_credenciamento_categorias
        # Apenas garante que seja salvo
        if commit:
            instance.save()

        return instance
