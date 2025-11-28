"""
Modelos de Banco de Dados usando SQLAlchemy
"""

from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float, ForeignKey, Text, DECIMAL
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class ClienteDB(Base):
    """Modelo de banco de dados para Cliente"""
    __tablename__ = "clientes"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=False, default="")
    email = Column(String(255), nullable=False, default="")
    data_cadastro = Column(DateTime, nullable=False, default=datetime.now)
    observacoes = Column(Text, nullable=False, default="")
    ativo = Column(Boolean, nullable=False, default=True)


class FuncionarioDB(Base):
    """Modelo de banco de dados para Funcionario"""
    __tablename__ = "funcionarios"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    telefone = Column(String(20), nullable=False, default="")
    email = Column(String(255), nullable=False, default="")
    cargo = Column(String(100), nullable=False, default="")
    data_admissao = Column(DateTime, nullable=False, default=datetime.now)
    salario = Column(Float, nullable=False, default=0.0)
    ativo = Column(Boolean, nullable=False, default=True)


class ServicoDB(Base):
    """Modelo de banco de dados para Servico"""
    __tablename__ = "servicos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String(255), nullable=False)
    descricao = Column(Text, nullable=False, default="")
    preco = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    duracao_minutos = Column(Integer, nullable=False, default=30)
    ativo = Column(Boolean, nullable=False, default=True)


class AgendamentoDB(Base):
    """Modelo de banco de dados para Agendamento"""
    __tablename__ = "agendamentos"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    cliente_id = Column(Integer, ForeignKey("clientes.id"), nullable=False)
    funcionario_id = Column(Integer, ForeignKey("funcionarios.id"), nullable=False)
    servico_id = Column(Integer, ForeignKey("servicos.id"), nullable=False)
    data_agendamento = Column(DateTime, nullable=True)
    horario_inicio = Column(DateTime, nullable=True)
    horario_fim = Column(DateTime, nullable=True)
    status = Column(String(50), nullable=False, default="agendado")
    observacoes = Column(Text, nullable=False, default="")
    valor_total = Column(DECIMAL(10, 2), nullable=False, default=0.00)
    
    # Relacionamentos (opcional, para facilitar queries)
    cliente = relationship("ClienteDB", foreign_keys=[cliente_id])
    funcionario = relationship("FuncionarioDB", foreign_keys=[funcionario_id])
    servico = relationship("ServicoDB", foreign_keys=[servico_id])

