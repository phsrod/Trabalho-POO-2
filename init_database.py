#!/usr/bin/env python3
"""
Script de Inicialização do Banco de Dados
Cria todas as tabelas necessárias no banco de dados
"""

from shared.database import init_db

if __name__ == "__main__":
    print("Inicializando banco de dados...")
    try:
        init_db()
        print("Banco de dados inicializado com sucesso!")
    except Exception as e:
        print(f"Erro ao inicializar banco de dados: {e}")
        import traceback
        traceback.print_exc()

