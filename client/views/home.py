import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
from .clientes import ClientesWidget
from .servicos import ServicosWidget
from .funcionarios import FuncionariosWidget
from .agendamentos import AgendamentosWidget
from .relatorios import RelatoriosWidget
from ..utils import StyleManager
from ..repositories import get_api_client
from ..models import Cliente, Funcionario, Agendamento

class HomeWindow:
    """Janela principal (dashboard) da aplicação administrativa"""
    
    def __init__(self, root: tk.Tk):
        self.root = root
        self.window = None
        self.current_widget = None
        self.content_frame = None
        self.scrollable_frame = None
        self.canvas = None
        self.scrollbar = None
        self.close_button = None
        
        # Cliente API para carregar dados
        self.api_client = get_api_client()
        
        # Labels dos cards de estatísticas (serão criados em create_stats_cards)
        self.stats_labels = {}
        
        # Flag para controlar atualização periódica
        self.auto_refresh_enabled = True
        self.auto_refresh_interval = 30000  # 30 segundos em milissegundos
        
        # ID para cancelar refresh pendente
        self._refresh_id = None

        # Configura os estilos globais
        StyleManager.configure_styles()
        
        self.create_window()
        # Carregar dados do dashboard após criar a janela
        self.load_dashboard_data()
        # Iniciar atualização periódica automática
        self.start_auto_refresh()
    
    def create_window(self):
        """Cria a janela principal"""
        self.window = tk.Toplevel(self.root)  # Usar o root passado
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
        agora = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.user_info.config(text="Administrador | " + agora)
        self.window.after(1000, self.update_time)  # atualiza a cada 1 segundo

    def create_stats_cards(self, parent):
        """Cria os cards de estatísticas"""
        stats_frame = ttk.Frame(parent, style='Main.TFrame')
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        cards_info = [
            ("Total de Clientes", "clientes"),
            ("Agendamentos Hoje", "agendamentos_hoje"),
            ("Receita Mensal", "receita_mensal"),
            ("Funcionários Ativos", "funcionarios")
        ]
        
        for i, (title, key) in enumerate(cards_info):
            card = ttk.Frame(stats_frame, style='Card.TFrame')
            card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(5 if i>0 else 0, 5))
            
            ttk.Label(card, text=title, style='Title.TLabel').pack(pady=(15, 5))
            # Criar label que será atualizado
            value_label = ttk.Label(card, text="Carregando...", style='Stat.TLabel')
            value_label.pack(pady=(0, 15))
            self.stats_labels[key] = value_label
    
    def create_navigation_menu(self, parent):
        """Cria o menu de navegação"""
        nav_frame = ttk.Frame(parent, style='Main.TFrame')
        nav_frame.pack(fill=tk.X, pady=(0, 20))
        
        menu_buttons = [
            ("Clientes", self.open_clients),
            ("Serviços", self.open_services),
            ("Funcionários", self.open_employees),
            ("Agendamentos", self.open_schedules),
            ("Relatórios", self.open_reports)
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
        
        Use o menu acima para navegar entre as diferentes funcionalidades.
        """
        
        ttk.Label(
            self.scrollable_frame, 
            text=welcome_text, 
            style='Subtitle.TLabel',
            justify=tk.CENTER
        ).pack(pady=10, padx=5)
    
    def clear_content(self):
        """Limpa o conteúdo atual de forma otimizada"""
        try:
            # Limpar referência primeiro para evitar problemas
            old_widget = self.current_widget
            self.current_widget = None
            
            # Destruir widgets de forma eficiente
            widgets_to_destroy = list(self.scrollable_frame.winfo_children())
            for widget in widgets_to_destroy:
                try:
                    widget.pack_forget()  # Remove do layout primeiro (mais rápido)
                except:
                    pass
            
            # Destruir widgets em lote (mais eficiente)
            for widget in widgets_to_destroy:
                try:
                    widget.destroy()
                except:
                    pass
            
            # Destruir widget antigo se existir
            if old_widget and hasattr(old_widget, 'main_frame'):
                try:
                    old_widget.main_frame.pack_forget()
                    old_widget.main_frame.destroy()
                except:
                    pass
        except:
            pass

    def show_content(self, widget_class, title):
        # Limpar conteúdo de forma otimizada
        self.clear_content()
        
        # Atualizar título e botão imediatamente
        self.content_title.config(text=title)
        self.close_button.pack(side=tk.RIGHT)
        
        # Criar widget diretamente (mais rápido) mas de forma otimizada
        try:
            self.current_widget = widget_class(self.scrollable_frame, dashboard_callback=self.notify_data_changed)
            self.current_widget.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
            # Atualizar scroll de forma assíncrona
            self.window.after(10, lambda: self.canvas.update_idletasks() or self.canvas.configure(scrollregion=self.canvas.bbox("all")))
            # Atualizar dashboard de forma assíncrona quando abrir uma seção (delay menor para resposta mais rápida)
            self.window.after(100, self.refresh_dashboard_quick)
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao criar widget: {str(e)}")

    def close_current_content(self):
        """Fecha o conteúdo atual e volta para a mensagem de boas-vindas"""
        self.show_welcome_message()
        # Atualizar dashboard de forma assíncrona quando fechar uma seção (mais rápido)
        if self.window and self.window.winfo_exists():
            self.window.after(50, self.refresh_dashboard_quick)
    
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
    
    def logout(self):
        if messagebox.askyesno("Confirmar", "Deseja realmente sair do sistema?"):
            self.window.destroy()
            if self.root:
                self.root.quit()
                self.root.destroy()
    
    def load_dashboard_data(self):
        """Carrega os dados do dashboard de forma assíncrona"""
        # Verificar se o servidor está rodando
        import requests
        try:
            response = requests.get("http://localhost:5000/api/health", timeout=2)
            if response.status_code != 200:
                raise Exception("Servidor não respondeu corretamente")
        except Exception as e:
            messagebox.showerror(
                "Servidor não disponível",
                "O servidor Flask não está rodando!\n\n"
                "Por favor, execute 'python server.py' em um terminal.\n\n"
                "A aplicação será fechada."
            )
            if self.window:
                self.window.destroy()
            if self.root:
                self.root.quit()
                self.root.destroy()
            return
        
        # Dashboard não precisa de loading - os cards já mostram "Carregando..."
        
        def on_clientes_loaded(clientes):
            # Não limpar dados antigos - apenas atualizar quando novos dados chegarem
            if clientes:  # Só atualizar se houver dados
                self.clientes = clientes
                # Agendar atualização da GUI na thread principal
                if self.window and self.window.winfo_exists():
                    self.window.after(0, self.update_clientes_count)
        
        def on_funcionarios_loaded(funcionarios):
            # Não limpar dados antigos - apenas atualizar quando novos dados chegarem
            if funcionarios:  # Só atualizar se houver dados
                self.funcionarios = funcionarios
                # Agendar atualização da GUI na thread principal
                if self.window and self.window.winfo_exists():
                    self.window.after(0, self.update_funcionarios_count)
        
        def on_agendamentos_loaded(agendamentos):
            # Não limpar dados antigos - apenas atualizar quando novos dados chegarem
            if agendamentos is not None:  # Atualizar mesmo se for lista vazia (None significa erro)
                self.agendamentos = agendamentos
                # Agendar atualização da GUI na thread principal
                if self.window and self.window.winfo_exists():
                    def update_stats():
                        if self.window and self.window.winfo_exists():
                            self.update_agendamentos_hoje()
                            self.update_receita_mensal()
                    self.window.after(0, update_stats)
        
        # NÃO inicializar listas vazias - manter dados antigos até novos chegarem
        # Isso evita que o dashboard fique zerado durante carregamento
        
        # Carregar dados usando threads
        self.api_client.load_clientes(on_clientes_loaded)
        self.api_client.load_funcionarios(on_funcionarios_loaded)
        self.api_client.load_agendamentos(on_agendamentos_loaded, force_reload=False)
    
    def refresh_dashboard(self):
        """Atualiza os dados do dashboard"""
        self.load_dashboard_data()
    
    def refresh_dashboard_quick(self):
        """Atualiza o dashboard rapidamente recarregando apenas os dados necessários"""
        # Recarregar dados de forma mais rápida, forçando atualização do cache
        def on_clientes_loaded(clientes):
            if clientes is not None:
                self.clientes = clientes
                if self.window and self.window.winfo_exists():
                    self.window.after(0, self.update_clientes_count)
        
        def on_funcionarios_loaded(funcionarios):
            if funcionarios is not None:
                self.funcionarios = funcionarios
                if self.window and self.window.winfo_exists():
                    self.window.after(0, self.update_funcionarios_count)
        
        def on_agendamentos_loaded(agendamentos):
            if agendamentos is not None:
                self.agendamentos = agendamentos
                if self.window and self.window.winfo_exists():
                    def update_stats():
                        if self.window and self.window.winfo_exists():
                            self.update_agendamentos_hoje()
                            self.update_receita_mensal()
                    self.window.after(0, update_stats)
        
        # Limpar cache para forçar recarregamento
        self.api_client._clientes = None
        self.api_client._funcionarios = None
        self.api_client._agendamentos = None
        
        # Carregar dados atualizados
        self.api_client.load_clientes(on_clientes_loaded)
        self.api_client.load_funcionarios(on_funcionarios_loaded)
        self.api_client.load_agendamentos(on_agendamentos_loaded, force_reload=True)
    
    def start_auto_refresh(self):
        """Inicia a atualização automática periódica do dashboard"""
        if self.auto_refresh_enabled and self.window:
            self.refresh_dashboard()
            # Agendar próxima atualização
            self.window.after(self.auto_refresh_interval, self.start_auto_refresh)
    
    def notify_data_changed(self):
        """Método público para ser chamado quando dados são alterados"""
        # Atualizar dashboard de forma assíncrona quando dados são alterados (para não travar)
        # Usar um delay menor para atualização mais rápida
        if self.window and self.window.winfo_exists():
            # Cancelar qualquer refresh pendente para evitar múltiplas chamadas
            if hasattr(self, '_refresh_id'):
                try:
                    self.window.after_cancel(self._refresh_id)
                except:
                    pass
            # Agendar novo refresh com delay menor (100ms) para resposta mais rápida
            self._refresh_id = self.window.after(100, self.refresh_dashboard_quick)
    
    def update_clientes_count(self):
        """Atualiza o contador de clientes"""
        try:
            if not self.window or not self.window.winfo_exists():
                return
            if 'clientes' in self.stats_labels and self.stats_labels['clientes'].winfo_exists():
                count = len([c for c in self.clientes if c.ativo])
                self.stats_labels['clientes'].config(text=str(count))
        except:
            return
    
    def update_funcionarios_count(self):
        """Atualiza o contador de funcionários"""
        try:
            if not self.window or not self.window.winfo_exists():
                return
            if 'funcionarios' in self.stats_labels and self.stats_labels['funcionarios'].winfo_exists():
                count = len([f for f in self.funcionarios if f.ativo])
                self.stats_labels['funcionarios'].config(text=str(count))
        except:
            return
    
    def update_agendamentos_hoje(self):
        """Atualiza o contador de agendamentos de hoje"""
        try:
            if not self.window or not self.window.winfo_exists():
                return
            if 'agendamentos_hoje' in self.stats_labels and self.stats_labels['agendamentos_hoje'].winfo_exists():
                hoje = datetime.now().date()
                count = 0
                
                for agendamento in self.agendamentos:
                    if not agendamento.data_agendamento:
                        continue
                    
                    # Normalizar data_agendamento para date
                    try:
                        if isinstance(agendamento.data_agendamento, datetime):
                            data_agendamento_date = agendamento.data_agendamento.date()
                        elif isinstance(agendamento.data_agendamento, date):
                            data_agendamento_date = agendamento.data_agendamento
                        else:
                            continue
                        
                        # Contar apenas agendamentos de hoje (não cancelados)
                        if data_agendamento_date == hoje and agendamento.status != 'cancelado':
                            count += 1
                    except (AttributeError, TypeError, ValueError):
                        continue
                
                self.stats_labels['agendamentos_hoje'].config(text=str(count))
        except:
            return
    
    def update_receita_mensal(self):
        """Atualiza a receita mensal"""
        try:
            if not self.window or not self.window.winfo_exists():
                return
            if 'receita_mensal' in self.stats_labels and self.stats_labels['receita_mensal'].winfo_exists():
                hoje = datetime.now()
                mes_atual = hoje.month
                ano_atual = hoje.year
                
                receita_total = 0.0
                
                for agendamento in self.agendamentos:
                    # Apenas agendamentos concluídos
                    if agendamento.status != 'concluido':
                        continue
                    
                    if not agendamento.data_agendamento:
                        continue
                    
                    # Normalizar data_agendamento para date
                    try:
                        if isinstance(agendamento.data_agendamento, datetime):
                            data_agendamento_date = agendamento.data_agendamento.date()
                        elif isinstance(agendamento.data_agendamento, date):
                            data_agendamento_date = agendamento.data_agendamento
                        else:
                            continue
                        
                        # Verificar se é do mês atual
                        if (isinstance(data_agendamento_date, date) and 
                            data_agendamento_date.month == mes_atual and 
                            data_agendamento_date.year == ano_atual):
                            receita_total += float(agendamento.valor_total)
                    except (AttributeError, TypeError, ValueError):
                        continue
                
                self.stats_labels['receita_mensal'].config(text=f"R$ {receita_total:.2f}")
        except:
            return
    
