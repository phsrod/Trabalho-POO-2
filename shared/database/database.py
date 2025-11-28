"""
Configuração do Banco de Dados
Usa SQLite para armazenamento local dos dados
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.pool import StaticPool
from pathlib import Path

# Base para os modelos
Base = declarative_base()

# Caminho do banco de dados
DB_DIR = Path("data")
DB_DIR.mkdir(exist_ok=True)
DB_PATH = DB_DIR / "barbearia.db"

# String de conexão SQLite
DATABASE_URL = f"sqlite:///{DB_PATH}"

# Engine do banco de dados
# Usa StaticPool para SQLite com check_same_thread=False para permitir threads
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
    echo=False
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    from . import models  # noqa: F401
    Base.metadata.create_all(bind=engine)

