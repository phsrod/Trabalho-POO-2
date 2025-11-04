#!/usr/bin/env python3
"""
Controller Principal da Aplicação
Gerencia o ciclo de vida e navegação da aplicação
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
            root = tk.Tk()
            root.withdraw()  # Esconder a janela raiz
            
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

