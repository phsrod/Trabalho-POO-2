"""
Rotas para gerenciamento de agendamentos
"""

from flask import request, jsonify
from datetime import datetime
from decimal import Decimal
from shared.database import SessionLocal, AgendamentoDB
from server.utils import agendamento_to_dict
from server.routes import api


@api.route('/agendamentos', methods=['GET'])
def get_agendamentos():
    """Retorna todos os agendamentos"""
    db = SessionLocal()
    try:
        agendamentos = db.query(AgendamentoDB).all()
        return jsonify([agendamento_to_dict(a) for a in agendamentos])
    finally:
        db.close()


@api.route('/agendamentos', methods=['POST'])
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
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

