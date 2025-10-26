# core/forms/__init__.py - IMPORTAÇÕES CENTRALIZADAS

# Formulários principais
from .usuario import UsuarioForm
from .feira import FeiraForm
from .congresso import CongressoForm

# Garantir que todos os formulários sejam exportados
__all__ = [
    'UsuarioForm',
    'FeiraForm',
    'CongressoForm',
]