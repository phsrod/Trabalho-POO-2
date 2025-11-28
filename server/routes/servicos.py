"""
Rotas para gerenciamento de serviços
"""

from flask import request, jsonify
from decimal import Decimal
from shared.database import SessionLocal, ServicoDB
from server.utils import servico_to_dict
from server.routes import api


@api.route('/servicos', methods=['GET'])
def get_servicos():
    """Retorna todos os serviços"""
    db = SessionLocal()
    try:
        servicos = db.query(ServicoDB).all()
        return jsonify([servico_to_dict(s) for s in servicos])
    finally:
        db.close()


@api.route('/servicos', methods=['POST'])
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
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

