#!/usr/bin/env python3
"""
Servidor Flask para API REST da Barbearia
Executa o servidor que gerencia o banco de dados e expõe endpoints REST
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from decimal import Decimal
from repositories.database import engine, SessionLocal, init_db
from repositories.db_models import ClienteDB, FuncionarioDB, ServicoDB, AgendamentoDB

# Configuração do Flask
app = Flask(__name__)
CORS(app)  # Permite requisições do cliente desktop

# Inicializar banco de dados
init_db()

# Funções auxiliares para conversão
def cliente_to_dict(cliente_db):
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

def funcionario_to_dict(funcionario_db):
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

def servico_to_dict(servico_db):
    """Converte ServicoDB para dicionário"""
    return {
        'id': servico_db.id,
        'nome': servico_db.nome,
        'descricao': servico_db.descricao,
        'preco': float(servico_db.preco),
        'duracao_minutos': servico_db.duracao_minutos,
        'ativo': servico_db.ativo
    }

def agendamento_to_dict(agendamento_db):
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

# ==================== ENDPOINTS CLIENTES ====================

@app.route('/api/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes"""
    db = SessionLocal()
    try:
        clientes = db.query(ClienteDB).all()
        return jsonify([cliente_to_dict(c) for c in clientes])
    finally:
        db.close()

@app.route('/api/clientes', methods=['POST'])
def save_clientes():
    """
    Salva/atualiza lista de clientes.
    IMPORTANTE: Não remove registros que não estão na requisição.
    Apenas atualiza ou cria novos registros baseado nos dados recebidos.
    """
    db = SessionLocal()
    try:
        data = request.json
        clientes_data = data.get('clientes', [])
        
        existing_ids = {c.id for c in db.query(ClienteDB).all()}
        
        for cliente_data in clientes_data:
            if cliente_data.get('id') and cliente_data['id'] in existing_ids:
                # Atualizar existente
                cliente_db = db.query(ClienteDB).filter(ClienteDB.id == cliente_data['id']).first()
                if cliente_db:
                    cliente_db.nome = cliente_data.get('nome', '')
                    cliente_db.telefone = cliente_data.get('telefone', '')
                    cliente_db.email = cliente_data.get('email', '')
                    if cliente_data.get('data_cadastro'):
                        cliente_db.data_cadastro = datetime.fromisoformat(cliente_data['data_cadastro'])
                    cliente_db.observacoes = cliente_data.get('observacoes', '')
                    cliente_db.ativo = cliente_data.get('ativo', True)
            else:
                # Criar novo
                cliente_db = ClienteDB(
                    nome=cliente_data.get('nome', ''),
                    telefone=cliente_data.get('telefone', ''),
                    email=cliente_data.get('email', ''),
                    data_cadastro=datetime.fromisoformat(cliente_data['data_cadastro']) if cliente_data.get('data_cadastro') else datetime.now(),
                    observacoes=cliente_data.get('observacoes', ''),
                    ativo=cliente_data.get('ativo', True)
                )
                db.add(cliente_db)
                db.flush()
                cliente_data['id'] = cliente_db.id
        
        # NÃO REMOVE registros que não estão na requisição
        # Isso evita perda de dados em caso de erro de rede ou carregamento incompleto
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

# ==================== ENDPOINTS FUNCIONARIOS ====================

@app.route('/api/funcionarios', methods=['GET'])
def get_funcionarios():
    """Retorna todos os funcionários"""
    db = SessionLocal()
    try:
        funcionarios = db.query(FuncionarioDB).all()
        return jsonify([funcionario_to_dict(f) for f in funcionarios])
    finally:
        db.close()

@app.route('/api/funcionarios', methods=['POST'])
def save_funcionarios():
    """
    Salva/atualiza lista de funcionários.
    IMPORTANTE: Não remove registros que não estão na requisição.
    Apenas atualiza ou cria novos registros baseado nos dados recebidos.
    """
    db = SessionLocal()
    try:
        data = request.json
        funcionarios_data = data.get('funcionarios', [])
        
        existing_ids = {f.id for f in db.query(FuncionarioDB).all()}
        
        for funcionario_data in funcionarios_data:
            if funcionario_data.get('id') and funcionario_data['id'] in existing_ids:
                funcionario_db = db.query(FuncionarioDB).filter(FuncionarioDB.id == funcionario_data['id']).first()
                if funcionario_db:
                    funcionario_db.nome = funcionario_data.get('nome', '')
                    funcionario_db.telefone = funcionario_data.get('telefone', '')
                    funcionario_db.email = funcionario_data.get('email', '')
                    funcionario_db.cargo = funcionario_data.get('cargo', '')
                    if funcionario_data.get('data_admissao'):
                        funcionario_db.data_admissao = datetime.fromisoformat(funcionario_data['data_admissao'])
                    funcionario_db.salario = funcionario_data.get('salario', 0.0)
                    funcionario_db.ativo = funcionario_data.get('ativo', True)
            else:
                funcionario_db = FuncionarioDB(
                    nome=funcionario_data.get('nome', ''),
                    telefone=funcionario_data.get('telefone', ''),
                    email=funcionario_data.get('email', ''),
                    cargo=funcionario_data.get('cargo', ''),
                    data_admissao=datetime.fromisoformat(funcionario_data['data_admissao']) if funcionario_data.get('data_admissao') else datetime.now(),
                    salario=funcionario_data.get('salario', 0.0),
                    ativo=funcionario_data.get('ativo', True)
                )
                db.add(funcionario_db)
                db.flush()
                funcionario_data['id'] = funcionario_db.id
        
        # NÃO REMOVE registros que não estão na requisição
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

# ==================== ENDPOINTS SERVIÇOS ====================

@app.route('/api/servicos', methods=['GET'])
def get_servicos():
    """Retorna todos os serviços"""
    db = SessionLocal()
    try:
        servicos = db.query(ServicoDB).all()
        return jsonify([servico_to_dict(s) for s in servicos])
    finally:
        db.close()

@app.route('/api/servicos', methods=['POST'])
def save_servicos():
    """
    Salva/atualiza lista de serviços.
    IMPORTANTE: Não remove registros que não estão na requisição.
    Apenas atualiza ou cria novos registros baseado nos dados recebidos.
    """
    db = SessionLocal()
    try:
        data = request.json
        servicos_data = data.get('servicos', [])
        
        existing_ids = {s.id for s in db.query(ServicoDB).all()}
        
        for servico_data in servicos_data:
            if servico_data.get('id') and servico_data['id'] in existing_ids:
                servico_db = db.query(ServicoDB).filter(ServicoDB.id == servico_data['id']).first()
                if servico_db:
                    servico_db.nome = servico_data.get('nome', '')
                    servico_db.descricao = servico_data.get('descricao', '')
                    servico_db.preco = Decimal(str(servico_data.get('preco', 0.00)))
                    servico_db.duracao_minutos = servico_data.get('duracao_minutos', 30)
                    servico_db.ativo = servico_data.get('ativo', True)
            else:
                servico_db = ServicoDB(
                    nome=servico_data.get('nome', ''),
                    descricao=servico_data.get('descricao', ''),
                    preco=Decimal(str(servico_data.get('preco', 0.00))),
                    duracao_minutos=servico_data.get('duracao_minutos', 30),
                    ativo=servico_data.get('ativo', True)
                )
                db.add(servico_db)
                db.flush()
                servico_data['id'] = servico_db.id
        
        # NÃO REMOVE registros que não estão na requisição
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

# ==================== ENDPOINTS AGENDAMENTOS ====================

@app.route('/api/agendamentos', methods=['GET'])
def get_agendamentos():
    """Retorna todos os agendamentos"""
    db = SessionLocal()
    try:
        agendamentos = db.query(AgendamentoDB).all()
        return jsonify([agendamento_to_dict(a) for a in agendamentos])
    finally:
        db.close()

@app.route('/api/agendamentos', methods=['POST'])
def save_agendamentos():
    """
    Salva/atualiza lista de agendamentos.
    IMPORTANTE: Não remove registros que não estão na requisição.
    Apenas atualiza ou cria novos registros baseado nos dados recebidos.
    """
    db = SessionLocal()
    try:
        data = request.json
        agendamentos_data = data.get('agendamentos', [])
        
        existing_ids = {a.id for a in db.query(AgendamentoDB).all()}
        
        for agendamento_data in agendamentos_data:
            if agendamento_data.get('id') and agendamento_data['id'] in existing_ids:
                agendamento_db = db.query(AgendamentoDB).filter(AgendamentoDB.id == agendamento_data['id']).first()
                if agendamento_db:
                    agendamento_db.cliente_id = agendamento_data.get('cliente_id', 0)
                    agendamento_db.funcionario_id = agendamento_data.get('funcionario_id', 0)
                    agendamento_db.servico_id = agendamento_data.get('servico_id', 0)
                    if agendamento_data.get('data_agendamento'):
                        agendamento_db.data_agendamento = datetime.fromisoformat(agendamento_data['data_agendamento'])
                    if agendamento_data.get('horario_inicio'):
                        agendamento_db.horario_inicio = datetime.fromisoformat(agendamento_data['horario_inicio'])
                    if agendamento_data.get('horario_fim'):
                        agendamento_db.horario_fim = datetime.fromisoformat(agendamento_data['horario_fim'])
                    agendamento_db.status = agendamento_data.get('status', 'agendado')
                    agendamento_db.observacoes = agendamento_data.get('observacoes', '')
                    agendamento_db.valor_total = Decimal(str(agendamento_data.get('valor_total', 0.00)))
            else:
                agendamento_db = AgendamentoDB(
                    cliente_id=agendamento_data.get('cliente_id', 0),
                    funcionario_id=agendamento_data.get('funcionario_id', 0),
                    servico_id=agendamento_data.get('servico_id', 0),
                    data_agendamento=datetime.fromisoformat(agendamento_data['data_agendamento']) if agendamento_data.get('data_agendamento') else None,
                    horario_inicio=datetime.fromisoformat(agendamento_data['horario_inicio']) if agendamento_data.get('horario_inicio') else None,
                    horario_fim=datetime.fromisoformat(agendamento_data['horario_fim']) if agendamento_data.get('horario_fim') else None,
                    status=agendamento_data.get('status', 'agendado'),
                    observacoes=agendamento_data.get('observacoes', ''),
                    valor_total=Decimal(str(agendamento_data.get('valor_total', 0.00)))
                )
                db.add(agendamento_db)
                db.flush()
                agendamento_data['id'] = agendamento_db.id
        
        # NÃO REMOVE registros que não estão na requisição
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

# ==================== ENDPOINT HEALTH CHECK ====================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Verifica se o servidor está rodando"""
    return jsonify({'status': 'ok', 'message': 'Servidor está rodando'})

if __name__ == '__main__':
    print("=" * 60)
    print("Servidor Flask da Barbearia")
    print("=" * 60)
    print(f"Servidor iniciando em http://localhost:5000")
    print("Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    app.run(host='localhost', port=5000, debug=False)
