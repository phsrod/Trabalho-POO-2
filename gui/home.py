import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
import datetime
from .clientes import ClientesWidget
from .servicos import ServicosWidget
from .funcionarios import FuncionariosWidget
from .agendamentos import AgendamentosWidget
from .relatorios import RelatoriosWidget

class HomeWindow:
    """Janela principal (dashboard) da aplicação administrativa"""
    
    def __init__(self):
        self.window = None
        self.current_widget = None
        self.content_frame = None
        self.scrollable_frame = None
        self.canvas = None
        self.scrollbar = None
        self.close_button = None
        self.create_window()
    
    def create_window(self):
        """Cria a janela principal"""
        self.window = tk.Toplevel()
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

        # Label que será atualizado
        self.user_info = ttk.Label(
            top_frame,
            style='Subtitle.TLabel'
        )
        self.user_info.pack(side=tk.LEFT, padx=10, pady=10)

        # Botão de logout
        logout_button = ttk.Button(
            top_frame,
            text="Sair",
            command=self.logout
        )
        logout_button.pack(side=tk.RIGHT, padx=10, pady=10)

        # Inicia a atualização em tempo real
        self.update_time()

    def update_time(self):
        """Atualiza a hora em tempo real no label"""
        agora = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.user_info.config(text="Administrador | " + agora)
        self.window.after(1000, self.update_time)  # atualiza a cada 1 segundo

    
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
        self.content_frame = ttk.Frame(parent, style='Card.TFrame')
        self.content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho da área de conteúdo com botão de fechar
        header_frame = ttk.Frame(self.content_frame)
        header_frame.pack(fill=tk.X, padx=5, pady=(5, 0))
        
        # Título da área de conteúdo
        self.content_title = ttk.Label(
            header_frame, 
            text="Bem-vindo ao Sistema Administrativo da Barbearia", 
            style='Title.TLabel'
        )
        self.content_title.pack(side=tk.LEFT)
        
        # Botão de fechar (inicialmente oculto)
        self.close_button = ttk.Button(
            header_frame,
            text="✕",
            command=self.close_current_content,
            width=3
        )
        self.close_button.pack(side=tk.RIGHT)
        self.close_button.pack_forget()  # Inicialmente oculto
        
        # Canvas e scrollbar para conteúdo rolável
        self.canvas = tk.Canvas(self.content_frame, bg='white', highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)
        
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Pack canvas e scrollbar
        self.canvas.pack(side="left", fill="both", expand=True, padx=(0, 0), pady=(0, 0))
        self.scrollbar.pack(side="right", fill="y", pady=(0, 0))
        
        # Bind mousewheel para scroll
        def _on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        self.canvas.bind("<MouseWheel>", _on_mousewheel)
        
        # Mostrar mensagem de boas-vindas inicial
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Mostra a mensagem de boas-vindas"""
        self.clear_content()
        self.content_title.config(text="Bem-vindo ao Sistema Administrativo da Barbearia")
        self.close_button.pack_forget()
        
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
            self.scrollable_frame, 
            text=welcome_text, 
            style='Subtitle.TLabel',
            justify=tk.CENTER
        ).pack(pady=10, padx=5)
    
    def clear_content(self):
        """Limpa o conteúdo atual"""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
        if self.current_widget:
            # Destruir o widget atual se existir
            if hasattr(self.current_widget, 'main_frame'):
                self.current_widget.main_frame.destroy()
            self.current_widget = None
    
    def show_content(self, widget_class, title):
        """Mostra um widget de conteúdo específico"""
        self.clear_content()
        self.content_title.config(text=title)
        self.close_button.pack(side=tk.RIGHT)
        
        # Criar nova instância do widget
        self.current_widget = widget_class(self.scrollable_frame)
        # O widget já tem seu main_frame que deve ser usado - esticado
        self.current_widget.main_frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
    
    def close_current_content(self):
        """Fecha o conteúdo atual e volta para a mensagem de boas-vindas"""
        self.show_welcome_message()
    
    def open_clients(self):
        """Abre a tela de gerenciamento de clientes"""
        try:
            self.show_content(ClientesWidget, "Gerenciamento de Clientes")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciamento de clientes: {str(e)}")
    
    def open_services(self):
        """Abre a tela de gerenciamento de serviços"""
        try:
            self.show_content(ServicosWidget, "Gerenciamento de Serviços")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciamento de serviços: {str(e)}")
    
    def open_employees(self):
        """Abre a tela de gerenciamento de funcionários"""
        try:
            self.show_content(FuncionariosWidget, "Gerenciamento de Funcionários")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciamento de funcionários: {str(e)}")
    
    def open_schedules(self):
        """Abre a tela de agendamentos"""
        try:
            self.show_content(AgendamentosWidget, "Visualização de Agendamentos")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir agendamentos: {str(e)}")
    
    def open_reports(self):
        """Abre a tela de relatórios"""
        try:
            self.show_content(RelatoriosWidget, "Relatórios e Estatísticas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir relatórios: {str(e)}")
    
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
