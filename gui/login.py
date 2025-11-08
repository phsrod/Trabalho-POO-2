import tkinter as tk
from tkinter import messagebox
from typing import Callable
from .styles import StyleManager


class LoginWindow:
    """Janela de login para administradores da barbearia"""

    def __init__(self, root: tk.Tk, on_login_success: Callable, on_cancel: Callable = None):
        self.root = root
        self.on_login_success = on_login_success
        self.on_cancel = on_cancel
        self.window = None
        self.create_window()

    def create_window(self):
        """Cria a janela de login"""
        self.window = self.root
        self.window.title("Barbearia - Login Administrativo")
        self.window.geometry("450x580")
        self.window.resizable(False, False)

        # Configurar estilos
        StyleManager.configure_styles()
        bg_color = StyleManager.get_color('light')
        self.window.configure(bg=bg_color)

        # Evento de fechamento
        self.window.protocol("WM_DELETE_WINDOW", self.cancel)
        self.center_window()

        # Container principal
        main_container = tk.Frame(self.window, bg=bg_color)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Frame central
        content_frame = tk.Frame(main_container, bg='#ffffff', relief='flat', bd=0)
        content_frame.place(relx=0.5, rely=0.5, anchor='center', width=400, height=520)

        # Linha superior
        tk.Frame(content_frame, bg=StyleManager.get_color('border'), height=2).pack(fill=tk.X, side=tk.TOP)

        # Frame interno
        inner_frame = tk.Frame(content_frame, bg='#ffffff')
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=40, pady=40)

        # Logo e título
        logo_frame = tk.Frame(inner_frame, bg='#ffffff')
        logo_frame.pack(pady=(0, 30))

        tk.Label(
            logo_frame, text="✂️", font=('Arial', 50),
            bg='#ffffff', fg=StyleManager.get_color('primary')
        ).pack()

        tk.Label(
            logo_frame, text="Barbearia Style",
            font=('Arial', 24, 'bold'),
            bg='#ffffff', fg=StyleManager.get_color('dark')
        ).pack(pady=(10, 5))

        tk.Label(
            logo_frame, text="Sistema Administrativo",
            font=('Arial', 11),
            bg='#ffffff', fg=StyleManager.get_color('gray')
        ).pack()

        # ==============================
        # Formulário usando GRID
        # ==============================
        form_frame = tk.Frame(inner_frame, bg='#ffffff')
        form_frame.pack(fill=tk.X, pady=(10, 0))
        form_frame.columnconfigure(1, weight=1)

        label_width = 10

        # Campo Usuário
        tk.Label(
            form_frame, text="Usuário",
            font=('Arial', 10, 'bold'),
            bg='#ffffff', fg=StyleManager.get_color('dark'),
            anchor='center', width=label_width
        ).grid(row=0, column=0, sticky='w', pady=(0, 10))

        self.username_entry = tk.Entry(
            form_frame,
            font=('Arial', 11),
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=StyleManager.get_color('primary'),
            highlightbackground=StyleManager.get_color('border'),
            bg='#ffffff',
            fg=StyleManager.get_color('dark'),
            insertbackground=StyleManager.get_color('dark')
        )
        self.username_entry.grid(row=0, column=1, sticky='ew', pady=(0, 10), ipady=8)

        # ==============================
        # Campo Senha (botão dentro do Entry)
        # ==============================
        tk.Label(
            form_frame, text="Senha",
            font=('Arial', 10, 'bold'),
            bg='#ffffff', fg=StyleManager.get_color('dark'),
            anchor='center', width=label_width
        ).grid(row=1, column=0, sticky='w', pady=(0, 10))

        password_container = tk.Frame(form_frame, bg='#ffffff')
        password_container.grid(row=1, column=1, sticky='ew', pady=(0, 10))
        password_container.grid_columnconfigure(0, weight=1)

        password_frame = tk.Frame(password_container, bg='#ffffff')
        password_frame.grid(row=0, column=0, sticky='ew')

        # Entry da senha
        self.password_entry = tk.Entry(
            password_frame,
            font=('Arial', 11),
            show="*",
            relief='solid',
            bd=1,
            highlightthickness=1,
            highlightcolor=StyleManager.get_color('primary'),
            highlightbackground=StyleManager.get_color('border'),
            bg='#ffffff',
            fg=StyleManager.get_color('dark'),
            insertbackground=StyleManager.get_color('dark')
        )
        self.password_entry.pack(fill='x', ipady=8)

        # Botão 👁️ fixo dentro do campo
        self.password_visible = False
        self.toggle_password_btn = tk.Button(
            password_frame,
            text="👁️",
            font=('Arial', 11),
            bg='#ffffff',
            fg=StyleManager.get_color('gray'),
            activebackground='#ffffff',
            activeforeground=StyleManager.get_color('dark'),
            relief='flat',
            bd=0,
            width=2,
            anchor='w',
            cursor='hand2',
            command=self.toggle_password_visibility
        )
        self.toggle_password_btn.place(relx=1.0, rely=0.5, anchor='e', x=-8, width=35)

        # Hover
        self.toggle_password_btn.bind("<Enter>", lambda e: self.toggle_password_btn.config(fg=StyleManager.get_color('primary')))
        self.toggle_password_btn.bind("<Leave>", lambda e: self.toggle_password_btn.config(fg=StyleManager.get_color('gray')))

        # ==============================
        # Link "Esqueci minha senha"
        # ==============================
        forgot_label = tk.Label(
            inner_frame,
            text="Esqueci minha senha",
            fg=StyleManager.get_color('gray'),
            font=('Arial', 9),
            bg='#ffffff',
            cursor="arrow"
        )
        forgot_label.pack(pady=(5, 20))

        # ==============================
        # Botão Entrar
        # ==============================
        button_container = tk.Frame(inner_frame, bg='#ffffff')
        button_container.pack(fill=tk.X, pady=(15, 0))

        self.login_button = tk.Button(
            button_container,
            text="Entrar",
            command=self.login,
            font=('Arial', 13, 'bold'),
            bg=StyleManager.get_color('primary'),
            fg='#ffffff',
            activebackground=StyleManager.get_color('primary_dark'),
            activeforeground='#ffffff',
            relief='flat',
            bd=0,
            cursor='hand2',
            height=1
        )
        self.login_button.pack(fill=tk.X, ipady=5)
        self.login_button.bind("<Enter>", lambda e: self.login_button.config(bg=StyleManager.get_color('primary_dark')))
        self.login_button.bind("<Leave>", lambda e: self.login_button.config(bg=StyleManager.get_color('primary')))

        # ==============================
        # Binds e foco
        # ==============================
        self.window.bind('<Return>', lambda e: self.login())
        self.username_entry.bind('<Return>', lambda e: self.password_entry.focus())
        self.password_entry.bind('<Return>', lambda e: self.login())
        self.username_entry.focus()

    def center_window(self):
        """Centraliza a janela na tela"""
        self.window.update_idletasks()
        width = 450
        height = 580
        screen_width = self.window.winfo_screenwidth()
        screen_height = self.window.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.window.geometry(f'{width}x{height}+{x}+{y}')

    def login(self):
        """Processa o login"""
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
            return

        if username == "admin" and password == "admin123":
            messagebox.showinfo("Sucesso", "Login realizado com sucesso!")
            for widget in self.window.winfo_children():
                widget.destroy()
            self.window.withdraw()
            self.on_login_success()
        else:
            messagebox.showerror("Erro", "Usuário ou senha incorretos.")
            self.password_entry.delete(0, tk.END)
            self.password_entry.focus()

    def toggle_password_visibility(self):
        """Alterna a visibilidade da senha"""
        self.password_visible = not self.password_visible
        if self.password_visible:
            self.password_entry.config(show="")
            self.toggle_password_btn.config(text="🙈")
        else:
            self.password_entry.config(show="*")
            self.toggle_password_btn.config(text="👁️")

    def cancel(self):
        """Cancela o login e fecha a aplicação"""
        if self.on_cancel:
            self.on_cancel()
        else:
            self.window.destroy()

    def run(self):
        """Executa a janela"""
        self.window.mainloop()
