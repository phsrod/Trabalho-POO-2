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
    echo=False  # Mude para True para ver SQL gerado
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Retorna uma sessão do banco de dados"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Inicializa o banco de dados criando todas as tabelas"""
    # Importar modelos para que sejam registrados na Base.metadata
    from . import db_models  # noqa: F401
    Base.metadata.create_all(bind=engine)

