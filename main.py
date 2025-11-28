#!/usr/bin/env python3
"""
Sistema Administrativo da Barbearia
Aplicação desktop para gerenciamento administrativo de barbearia

Ponto de entrada principal da aplicação
"""

from client.controllers import BarbeariaApp

def main():
    """Função principal - apenas inicia a aplicação"""
    try:
        app = BarbeariaApp()
        app.start()
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {str(e)}")

if __name__ == "__main__":
    main()
