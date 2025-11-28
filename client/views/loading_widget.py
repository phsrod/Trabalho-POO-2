"""
Componente de Loading Reutilizável
Exibe uma mensagem de carregamento visual integrada ao layout, sem usar messagebox
"""

import tkinter as tk
from tkinter import ttk


class LoadingWidget:
    """Widget de carregamento visual integrado ao layout"""
    
    def __init__(self, parent, message="Carregando..."):
        """
        Cria um widget de loading
        
        Args:
            parent: Widget pai onde o loading será exibido (deve ser um frame que aceita pack)
            message: Mensagem a ser exibida (padrão: "Carregando...")
        """
        self.parent = parent
        self.message = message
        self.loading_frame = None
        self._animation_id = None
        self._dots = 0
        
    def show(self):
        """Mostra o widget de loading integrado ao layout"""
        if self.loading_frame is not None:
            return  # Já está visível
        
        try:
            # Criar frame de loading que ocupa o espaço disponível
            self.loading_frame = ttk.Frame(self.parent)
            self.loading_frame.pack(fill=tk.BOTH, expand=True)
            
            # Container centralizado
            center_container = ttk.Frame(self.loading_frame)
            center_container.pack(expand=True)
            
            # Label com mensagem
            self.loading_label = ttk.Label(
                center_container,
                text=self.message,
                font=('Arial', 11),
                foreground='#666'
            )
            self.loading_label.pack(pady=20)
            
            # Iniciar animação de pontos
            self._animate_dots()
        except:
            pass
    
    def hide(self):
        """Esconde o widget de loading"""
        if self.loading_frame is not None:
            if self._animation_id is not None:
                try:
                    root = self.parent.winfo_toplevel()
                    root.after_cancel(self._animation_id)
                except:
                    pass
                self._animation_id = None
            try:
                if self.loading_frame.winfo_exists():
                    self.loading_frame.pack_forget()
                    self.loading_frame.destroy()
            except:
                pass
            self.loading_frame = None
            self._dots = 0
    
    def _animate_dots(self):
        """Anima os pontos no final da mensagem"""
        if self.loading_frame is None or not self.loading_frame.winfo_exists():
            return
        
        dots = "." * (self._dots % 4)  # 0, 1, 2, 3 pontos
        try:
            if self.loading_label.winfo_exists():
                self.loading_label.config(text=f"{self.message}{dots}")
        except:
            return
        
        self._dots += 1
        root = self.parent.winfo_toplevel()
        if root and root.winfo_exists():
            self._animation_id = root.after(500, self._animate_dots)
    
    def update_message(self, message):
        """Atualiza a mensagem de loading"""
        self.message = message
        if self.loading_frame is not None and self.loading_label.winfo_exists():
            dots = "." * (self._dots % 4)
            try:
                self.loading_label.config(text=f"{message}{dots}")
            except:
                pass

