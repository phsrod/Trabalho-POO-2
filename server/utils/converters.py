"""
Funções de conversão entre modelos de banco e dicionários
"""

from datetime import datetime
from decimal import Decimal
from shared.database import ClienteDB, FuncionarioDB, ServicoDB, AgendamentoDB


def cliente_to_dict(cliente_db: ClienteDB) -> dict:
    """Converte ClienteDB para dicionário"""
    return {
        'id': cliente_db.id,
        'nome': cliente_db.nome,
        'telefone': cliente_db.telefone,
        'email': cliente_db.email,
        'data_cadastro': cliente_db.data_cadastro.isoformat() if cliente_db.data_cadastro else None,
        'observacoes': cliente_db.observacoes,
        'ativo': cliente_db.ativo
    }


def funcionario_to_dict(funcionario_db: FuncionarioDB) -> dict:
    """Converte FuncionarioDB para dicionário"""
    return {
        'id': funcionario_db.id,
        'nome': funcionario_db.nome,
        'telefone': funcionario_db.telefone,
        'email': funcionario_db.email,
        'cargo': funcionario_db.cargo,
        'data_admissao': funcionario_db.data_admissao.isoformat() if funcionario_db.data_admissao else None,
        'salario': funcionario_db.salario,
        'ativo': funcionario_db.ativo
    }


def servico_to_dict(servico_db: ServicoDB) -> dict:
    """Converte ServicoDB para dicionário"""
    return {
        'id': servico_db.id,
        'nome': servico_db.nome,
        'descricao': servico_db.descricao,
        'preco': float(servico_db.preco),
        'duracao_minutos': servico_db.duracao_minutos,
        'ativo': servico_db.ativo
    }


def agendamento_to_dict(agendamento_db: AgendamentoDB) -> dict:
    """Converte AgendamentoDB para dicionário"""
    return {
        'id': agendamento_db.id,
        'cliente_id': agendamento_db.cliente_id,
        'funcionario_id': agendamento_db.funcionario_id,
        'servico_id': agendamento_db.servico_id,
        'data_agendamento': agendamento_db.data_agendamento.isoformat() if agendamento_db.data_agendamento else None,
        'horario_inicio': agendamento_db.horario_inicio.isoformat() if agendamento_db.horario_inicio else None,
        'horario_fim': agendamento_db.horario_fim.isoformat() if agendamento_db.horario_fim else None,
        'status': agendamento_db.status,
        'observacoes': agendamento_db.observacoes,
        'valor_total': float(agendamento_db.valor_total)
    }

