# core/models/__init__.py - IMPORTAÇÕES CENTRALIZADAS

# Modelos principais
from .usuario import Usuario

# Modelos externos (não gerenciados - Directus)
from .feira import Feira, Congresso

# Garantir que todos os modelos sejam exportados
__all__ = [
    # Principais
    'Usuario',

    # Externos (Directus)
    'Feira',
    'Congresso',
]