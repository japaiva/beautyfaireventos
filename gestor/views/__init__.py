# gestor/views/__init__.py

# Dashboard
from .dashboard import dashboard, home

# Usuário
from .usuario import (
    usuario_list,
    usuario_create,
    usuario_update,
    usuario_delete
)

# Feira
from .feira import (
    feira_list,
    feira_create,
    feira_update,
    feira_delete
)

# Congresso
from .congresso import (
    congresso_list,
    congresso_create,
    congresso_update,
    congresso_delete
)