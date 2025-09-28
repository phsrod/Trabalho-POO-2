import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable

class LoginWindow:
    """Janela de login para administradores da barbearia"""
    
    def __init__(self, on_login_success: Callable):
        self.on_login_success = on_login_success
        self.window = None
        self.create_window()
    
    def create_window(self):
        """Cria a janela de login"""
        self.window = tk.Toplevel()
        self.window.title("Barbearia - Login Administrativo")
        self.window.geometry("400x300")
        self.window.resizable(False, False)
        self.window.configure(bg='#f0f0f0')
        
        # Centralizar a janela
        self.center_window()
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Sistema Administrativo", 
            font=('Arial', 16, 'bold')
        )
        title_label.pack(pady=(0, 10))
        
        subtitle_label = ttk.Label(
            main_frame, 
            text="Barbearia Style", 
            font=('Arial', 12)
        )
        subtitle_label.pack(pady=(0, 30))
        
        # Frame do formulário
        form_frame = ttk.Frame(main_frame)
        form_frame.pack(fill=tk.X, pady=10)
        
        # Usuário
        ttk.Label(form_frame, text="Usuário:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.username_entry = ttk.Entry(form_frame, width=25, font=('Arial', 10))
        self.username_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Senha
        ttk.Label(form_frame, text="Senha:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.password_entry = ttk.Entry(form_frame, width=25, show="*", font=('Arial', 10))
        self.password_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)

        # Recuperar senha
        forgot_password_label = tk.Label(
            form_frame, 
            text="Esqueci minha senha", 
            fg="blue", 
            cursor="hand2", 
            font=('Arial', 9, 'underline')
        )
        forgot_password_label.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=(5, 0))

        # Bind para simular a recuperação de senha
        forgot_password_label.bind("<Button-1>", lambda e: self.recover_password())
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(30, 0))
        
        login_button = ttk.Button(
            button_frame, 
            text="Entrar", 
            command=self.login,
            style='Accent.TButton'
        )
        login_button.pack(side=tk.LEFT, padx=(0, 10))
        
        cancel_button = ttk.Button(
            button_frame, 
            text="Sair", 
            command=self.cancel
        )
        cancel_button.pack(side=tk.LEFT)
        
        # Configurar estilo do botão de login
        style.configure('Accent.TButton', foreground='white', background='#0078d4')
        
        # Bind Enter key
        self.window.bind('<Return>', lambda e: self.login())
        
        # Focus no campo usuário
        self.username_entry.focus()
    
    def center_window(self):
        """Centraliza a janela na tela"""
        self.window.update_idletasks()
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = (self.window.winfo_screenwidth() // 2) - (width // 2)
        y = (self.window.winfo_screenheight() // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')
    
    def login(self):
        """Processa o login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()
        
        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return
        
        # Validação simples (em produção, isso seria feito com banco de dados)
        if username == "admin" and password == "admin123":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            self.window.destroy()
            self.on_login_success()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()
    
    def recover_password(self):
        """Simula a recuperação de senha"""
        messagebox.showinfo(
            "Recuperar senha",
            "Função de recuperação de senha ainda não implementada."
        )

    def cancel(self):
        """Cancela o login e fecha a aplicação"""
        self.window.destroy()
    
    def run(self):
        """Executa a janela de login"""
        self.window.mainloop()
