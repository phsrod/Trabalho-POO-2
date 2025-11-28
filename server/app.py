"""
Aplicação Flask principal
"""

from flask import Flask
from flask_cors import CORS
from shared.database import init_db
from server.routes import api


def create_app():
    """Cria e configura a aplicação Flask"""
    app = Flask(__name__)
    CORS(app)
    
    # Registrar rotas
    app.register_blueprint(api)
    
    # Inicializar banco de dados
    init_db()
    
    return app

