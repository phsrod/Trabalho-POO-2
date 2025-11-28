"""
Modelos e configuração de banco de dados compartilhados
"""

from .database import Base, engine, SessionLocal, init_db
from .models import ClienteDB, FuncionarioDB, ServicoDB, AgendamentoDB

__all__ = [
    'Base', 'engine', 'SessionLocal', 'init_db',
    'ClienteDB', 'FuncionarioDB', 'ServicoDB', 'AgendamentoDB'
]

