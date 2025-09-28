#!/usr/bin/env python3
"""
Sistema Administrativo da Barbearia
Aplicação desktop para gerenciamento administrativo de barbearia
"""

import tkinter as tk
from tkinter import messagebox
from gui import LoginWindow, HomeWindow, StyleManager

class BarbeariaApp:
    """Classe principal da aplicação"""
    
    def __init__(self):
        self.home_window = None
    
    def start(self):
        """Inicia a aplicação"""
        try:
            # Configurar estilos
            StyleManager.configure_styles()
            
            # Mostra a tela de login
            login_window = LoginWindow(self.on_login_success)
            login_window.run()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar a aplicação: {str(e)}")
    
    def on_login_success(self):
        """Callback chamado quando o login é bem-sucedido"""
        try:
            # Cria e mostra a janela principal
            self.home_window = HomeWindow()
            self.home_window.run()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a janela principal: {str(e)}")

def main():
    """Função principal"""
    try:
        app = BarbeariaApp()
        app.start()
    except KeyboardInterrupt:
        print("\nAplicação interrompida pelo usuário.")
    except Exception as e:
        print(f"Erro fatal: {str(e)}")

if __name__ == "__main__":
    main()
