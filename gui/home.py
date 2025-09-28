import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable
import datetime

class HomeWindow:
    """Janela principal (dashboard) da aplicação administrativa"""
    
    def __init__(self):
        self.window = None
        self.create_window()
    
    def create_window(self):
        """Cria a janela principal"""
        self.window = tk.Tk()
        self.window.title("Barbearia - Sistema Administrativo")
        self.window.geometry("1200x800")
        self.window.state('zoomed')  # Maximizar no Windows
        self.window.configure(bg='#f5f5f5')
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        self.configure_styles(style)
        
        # Criar layout principal
        self.create_layout()
    
    def configure_styles(self, style):
        """Configura os estilos da interface"""
        # Estilo do menu
        style.configure('Menu.TButton', padding=(10, 5))
        
        # Estilo dos cards
        style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)
        
        # Estilo dos títulos
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='white')
        
        # Estilo dos subtítulos
        style.configure('Subtitle.TLabel', font=('Arial', 10), background='white', foreground='#666')
    
    def create_layout(self):
        """Cria o layout principal da janela"""
        # Barra superior
        self.create_top_bar()
        
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título principal
        title_label = ttk.Label(
            main_frame, 
            text="Dashboard Administrativo", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Cards de estatísticas
        self.create_stats_cards(main_frame)
        
        # Menu de navegação
        self.create_navigation_menu(main_frame)
        
        # Área de conteúdo principal
        self.create_content_area(main_frame)
    
    def create_top_bar(self):
        """Cria a barra superior com informações do usuário"""
        top_frame = ttk.Frame(self.window, style='Card.TFrame')
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Informações do usuário
        user_info = ttk.Label(
            top_frame, 
            text="Administrador | " + datetime.datetime.now().strftime("%d/%m/%Y %H:%M"),
            style='Subtitle.TLabel'
        )
        user_info.pack(side=tk.LEFT, padx=10, pady=10)
        
        # Botão de logout
        logout_button = ttk.Button(
            top_frame, 
            text="Sair", 
            command=self.logout
        )
        logout_button.pack(side=tk.RIGHT, padx=10, pady=10)
    
    def create_stats_cards(self, parent):
        """Cria os cards de estatísticas"""
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Card 1 - Clientes
        client_card = ttk.Frame(stats_frame, style='Card.TFrame')
        client_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(client_card, text="Total de Clientes", style='Title.TLabel').pack(pady=(15, 5))
        ttk.Label(client_card, text="0", font=('Arial', 24, 'bold'), background='white').pack(pady=(0, 15))
        
        # Card 2 - Agendamentos Hoje
        schedule_card = ttk.Frame(stats_frame, style='Card.TFrame')
        schedule_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(schedule_card, text="Agendamentos Hoje", style='Title.TLabel').pack(pady=(15, 5))
        ttk.Label(schedule_card, text="0", font=('Arial', 24, 'bold'), background='white').pack(pady=(0, 15))
        
        # Card 3 - Receita Mensal
        revenue_card = ttk.Frame(stats_frame, style='Card.TFrame')
        revenue_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(revenue_card, text="Receita Mensal", style='Title.TLabel').pack(pady=(15, 5))
        ttk.Label(revenue_card, text="R$ 0,00", font=('Arial', 24, 'bold'), background='white').pack(pady=(0, 15))
        
        # Card 4 - Funcionários
        employee_card = ttk.Frame(stats_frame, style='Card.TFrame')
        employee_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        ttk.Label(employee_card, text="Funcionários Ativos", style='Title.TLabel').pack(pady=(15, 5))
        ttk.Label(employee_card, text="0", font=('Arial', 24, 'bold'), background='white').pack(pady=(0, 15))
    
    def create_navigation_menu(self, parent):
        """Cria o menu de navegação"""
        nav_frame = ttk.Frame(parent)
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Botões do menu
        menu_buttons = [
            ("Clientes", self.open_clients),
            ("Serviços", self.open_services),
            ("Funcionários", self.open_employees),
            ("Agendamentos", self.open_schedules),
            ("Relatórios", self.open_reports),
            ("Configurações", self.open_settings)
        ]
        
        for i, (text, command) in enumerate(menu_buttons):
            btn = ttk.Button(
                nav_frame, 
                text=text, 
                command=command,
                style='Menu.TButton'
            )
            btn.pack(side=tk.LEFT, padx=(0, 10) if i < len(menu_buttons) - 1 else 0)
    
    def create_content_area(self, parent):
        """Cria a área de conteúdo principal"""
        content_frame = ttk.Frame(parent, style='Card.TFrame')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título da área de conteúdo
        ttk.Label(
            content_frame, 
            text="Bem-vindo ao Sistema Administrativo da Barbearia", 
            style='Title.TLabel'
        ).pack(pady=20)
        
        # Texto de boas-vindas
        welcome_text = """
        Este sistema permite gerenciar todos os aspectos administrativos da barbearia:
        
        • Cadastro e gerenciamento de clientes
        • Controle de serviços oferecidos
        • Gestão de funcionários
        • Visualização de agendamentos
        • Relatórios e estatísticas
        • Configurações do sistema
        
        Use o menu acima para navegar entre as diferentes funcionalidades.
        """
        
        ttk.Label(
            content_frame, 
            text=welcome_text, 
            style='Subtitle.TLabel',
            justify=tk.LEFT
        ).pack(pady=20, padx=20)
    
    def open_clients(self):
        """Abre a tela de gerenciamento de clientes"""
        messagebox.showinfo("Info", "Funcionalidade de Clientes será implementada em breve.")
    
    def open_services(self):
        """Abre a tela de gerenciamento de serviços"""
        messagebox.showinfo("Info", "Funcionalidade de Serviços será implementada em breve.")
    
    def open_employees(self):
        """Abre a tela de gerenciamento de funcionários"""
        messagebox.showinfo("Info", "Funcionalidade de Funcionários será implementada em breve.")
    
    def open_schedules(self):
        """Abre a tela de agendamentos"""
        messagebox.showinfo("Info", "Funcionalidade de Agendamentos será implementada em breve.")
    
    def open_reports(self):
        """Abre a tela de relatórios"""
        messagebox.showinfo("Info", "Funcionalidade de Relatórios será implementada em breve.")
    
    def open_settings(self):
        """Abre a tela de configurações"""
        messagebox.showinfo("Info", "Funcionalidade de Configurações será implementada em breve.")
    
    def logout(self):
        """Realiza logout do sistema"""
        if messagebox.askyesno("Confirmar", "Deseja realmente sair do sistema?"):
            self.window.destroy()
    
    def run(self):
        """Executa a janela principal"""
        self.window.mainloop()
