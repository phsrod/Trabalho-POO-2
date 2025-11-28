"""
Rotas para gerenciamento de clientes
"""

from flask import request, jsonify
from datetime import datetime
from shared.database import SessionLocal, ClienteDB
from server.utils import cliente_to_dict
from server.routes import api


@api.route('/clientes', methods=['GET'])
def get_clientes():
    """Retorna todos os clientes"""
    db = SessionLocal()
    try:
        clientes = db.query(ClienteDB).all()
        return jsonify([cliente_to_dict(c) for c in clientes])
    finally:
        db.close()


@api.route('/clientes', methods=['POST'])
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
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

