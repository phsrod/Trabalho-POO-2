"""
Rotas para gerenciamento de funcionários
"""

from flask import request, jsonify
from datetime import datetime
from shared.database import SessionLocal, FuncionarioDB
from server.utils import funcionario_to_dict
from server.routes import api


@api.route('/funcionarios', methods=['GET'])
def get_funcionarios():
    """Retorna todos os funcionários"""
    db = SessionLocal()
    try:
        funcionarios = db.query(FuncionarioDB).all()
        return jsonify([funcionario_to_dict(f) for f in funcionarios])
    finally:
        db.close()


@api.route('/funcionarios', methods=['POST'])
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
        
        db.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.rollback()
        return jsonify({'success': False, 'error': str(e)}), 500
    finally:
        db.close()

