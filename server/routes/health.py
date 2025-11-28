"""
Rota de health check
"""

from flask import jsonify
from server.routes import api


@api.route('/health', methods=['GET'])
def health_check():
    """Verifica se o servidor está rodando"""
    return jsonify({'status': 'ok', 'message': 'Servidor está rodando'})

