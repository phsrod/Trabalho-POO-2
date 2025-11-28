"""
Rotas da API REST
"""

from flask import Blueprint

# Criar blueprint para as rotas
api = Blueprint('api', __name__, url_prefix='/api')

# Importar todas as rotas (após criar o blueprint para evitar import circular)
from . import clientes, funcionarios, servicos, agendamentos, health  # noqa: E402

__all__ = ['api']

