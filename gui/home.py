import tkinter as tk
from tkinter import ttk, messagebox
from typing import Callable, Optional
import datetime
from .clientes import ClientesWidget
from .servicos import ServicosWidget
from .funcionarios import FuncionariosWidget
from .agendamentos import AgendamentosWidget
from .relatorios import RelatoriosWidget
from .styles import StyleManager  # Importando o StyleManager

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

        # Configura os estilos globais
        StyleManager.configure_styles()
        
        self.create_window()
    
    def create_window(self):
        """Cria a janela principal"""
        self.window = tk.Toplevel()
        self.window.title("Barbearia - Sistema Administrativo")
        self.window.geometry("1200x800")
        self.window.state('zoomed')  # Maximizar no Windows
        self.window.configure(bg=StyleManager.get_color('light'))
        
        # Cria layout principal
        self.create_layout()
    
    def create_layout(self):
        """Cria o layout principal da janela"""
        # Barra superior
        self.create_top_bar()
        
        # Frame principal
        main_frame = ttk.Frame(self.window, style='Main.TFrame', padding="20")
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
        top_frame = ttk.Frame(self.window, style='Header.TFrame')
        top_frame.pack(fill=tk.X, padx=10, pady=10)

        # Label que será atualizado
        self.user_info = ttk.Label(
            top_frame,
            style='Header.TLabel'
        )
        self.user_info.pack(side=tk.LEFT, padx=10, pady=10)

        # Botão de logout
        logout_button = ttk.Button(
            top_frame,
            text="Sair",
            command=self.logout,
            style='Danger.TButton'
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
        stats_frame = ttk.Frame(parent, style='Main.TFrame')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        cards_info = [
            ("Total de Clientes", "0"),
            ("Agendamentos Hoje", "0"),
            ("Receita Mensal", "R$ 0,00"),
            ("Funcionários Ativos", "0")
        ]
        
        for i, (title, value) in enumerate(cards_info):
            card = ttk.Frame(stats_frame, style='Card.TFrame')
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5 if i>0 else 0, 5))
            
            ttk.Label(card, text=title, style='Title.TLabel').pack(pady=(15, 5))
            ttk.Label(card, text=value, style='Stat.TLabel').pack(pady=(0, 15))
    
    def create_navigation_menu(self, parent):
        """Cria o menu de navegação"""
        nav_frame = ttk.Frame(parent, style='Main.TFrame')
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
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
        header_frame = ttk.Frame(self.content_frame, style='Main.TFrame')
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
            width=3,
            style='Danger.TButton'
        )
        self.close_button.pack(side=tk.RIGHT)
        self.close_button.pack_forget()
        
        # Canvas e scrollbar para conteúdo rolável
        self.canvas = tk.Canvas(self.content_frame, bg=StyleManager.get_color('white'), highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self.content_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas, style='Content.TFrame')

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas_window = self.canvas.create_window((0,0), window=self.scrollable_frame, anchor="nw")

        self.canvas.bind("<Configure>", lambda e: self.canvas.itemconfig(self.canvas_window, width=e.width))
        self.scrollable_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        self.canvas.pack(side="left", fill="both", expand=True, padx=(10, 0), pady=(10, 0))
        self.scrollbar.pack(side="right", fill="y", pady=(10, 0))

        self.canvas.bind("<MouseWheel>", lambda event: self.canvas.yview_scroll(int(-1*(event.delta/120)), "units"))

        # Mensagem de boas-vindas inicial
        self.show_welcome_message()
    
    def show_welcome_message(self):
        """Mostra a mensagem de boas-vindas"""
        self.clear_content()
        self.content_title.config(text="Bem-vindo ao Sistema Administrativo da Barbearia")
        self.close_button.pack_forget()
        
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
        if self.current_widget and hasattr(self.current_widget, 'main_frame'):
            self.current_widget.main_frame.destroy()
            self.current_widget = None

    def show_content(self, widget_class, title):
        self.clear_content()
        self.content_title.config(text=title)
        self.close_button.pack(side=tk.RIGHT)
        self.current_widget = widget_class(self.scrollable_frame)
        self.current_widget.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.canvas.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def close_current_content(self):
        """Fecha o conteúdo atual e volta para a mensagem de boas-vindas"""
        self.show_welcome_message()
    
    def open_clients(self):
        try:
            self.show_content(ClientesWidget, "Gerenciamento de Clientes")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciamento de clientes: {str(e)}")
    
    def open_services(self):
        try:
            self.show_content(ServicosWidget, "Gerenciamento de Serviços")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciamento de serviços: {str(e)}")
    
    def open_employees(self):
        try:
            self.show_content(FuncionariosWidget, "Gerenciamento de Funcionários")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir gerenciamento de funcionários: {str(e)}")
    
    def open_schedules(self):
        try:
            self.show_content(AgendamentosWidget, "Visualização de Agendamentos")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir agendamentos: {str(e)}")
    
    def open_reports(self):
        try:
            self.show_content(RelatoriosWidget, "Relatórios e Estatísticas")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao abrir relatórios: {str(e)}")
    
    def open_settings(self):
        messagebox.showinfo("Info", "Funcionalidade de Configurações será implementada em breve.")
    
    def logout(self):
        if messagebox.askyesno("Confirmar", "Deseja realmente sair do sistema?"):
            self.window.destroy()
    
    def run(self):
        self.window.mainloop()
