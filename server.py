#!/usr/bin/env python3
"""
Ponto de entrada do servidor Flask
"""

from server import create_app

if __name__ == '__main__':
    app = create_app()
    
    print("=" * 60)
    print("Servidor Flask da Barbearia")
    print("=" * 60)
    print("Servidor iniciando em http://localhost:5000")
    print("Pressione Ctrl+C para parar o servidor")
    print("=" * 60)
    
    app.run(host='localhost', port=5000, debug=False)
