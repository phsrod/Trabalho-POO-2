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
        self.root = None
        self.home_window = None
        self.login_window = None
    
    def start(self):
        """Inicia a aplicação"""
        try:
            self.root = tk.Tk()
            
            # Configurar estilos
            StyleManager.configure_styles()
            
            # Mostra a tela de login
            self.login_window = LoginWindow(self.root, self.on_login_success, self.on_login_cancel)
            self.login_window.run()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao iniciar a aplicação: {str(e)}")
        finally:
            # Garantir que o root seja destruído ao sair
            if self.root:
                try:
                    self.root.quit()
                    self.root.destroy()
                except:
                    pass
    
    def on_login_success(self):
        """Callback chamado quando o login é bem-sucedido"""
        try:
            # Cria e mostra a janela principal
            self.home_window = HomeWindow(self.root)
            # Configurar protocolo de fechamento para encerrar o programa
            self.home_window.window.protocol("WM_DELETE_WINDOW", self.on_window_close)
            # Aguardar até que a janela principal seja fechada
            self.home_window.window.wait_window()
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir a janela principal: {str(e)}")
    
    def on_login_cancel(self):
        """Callback chamado quando o login é cancelado"""
        if self.root:
            self.root.quit()
            self.root.destroy()
    
    def on_window_close(self):
        """Handler chamado quando a janela principal é fechada"""
        if messagebox.askyesno("Confirmar", "Deseja realmente sair do sistema?"):
            if self.home_window:
                self.home_window.window.destroy()
            if self.root:
                self.root.quit()
                self.root.destroy()

