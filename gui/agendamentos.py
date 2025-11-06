import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional, Tuple, Callable
from models import Agendamento, Cliente, Funcionario, Servico
from datetime import datetime, timedelta, date
from decimal import Decimal
from repositories import get_data_manager

class AgendamentosWindow:
    """Janela de visualização de agendamentos"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.window = None
        self.agendamentos: List[Agendamento] = []
        self.clientes: List[Cliente] = []
        self.funcionarios: List[Funcionario] = []
        self.servicos: List[Servico] = []
        self.create_window()
        self.load_sample_data()
        self.refresh_agendamentos_list()
    
    def create_window(self):
        """Cria a janela de agendamentos"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Visualização de Agendamentos")
        self.window.geometry("1200x700")
        self.window.configure(bg='#f5f5f5')
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        self.configure_styles(style)
        
        # Criar layout
        self.create_layout()
    
    def configure_styles(self, style):
        """Configura os estilos da interface"""
        style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='white')
        style.configure('Subtitle.TLabel', font=('Arial', 10), background='white', foreground='#666')
        style.configure('Action.TButton', padding=(8, 4))
        
        # Estilos para status
        style.configure('Agendado.TLabel', foreground='#0078d4')
        style.configure('Confirmado.TLabel', foreground='#107c10')
        style.configure('EmAndamento.TLabel', foreground='#ff8c00')
        style.configure('Concluido.TLabel', foreground='#107c10')
        style.configure('Cancelado.TLabel', foreground='#d13438')
    
    def create_layout(self):
        """Cria o layout principal"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Visualização de Agendamentos", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Filtros
        self.create_filters(main_frame)
        
        # Lista de agendamentos
        self.create_agendamentos_list(main_frame)
    
    def create_filters(self, parent):
        """Cria os filtros de agendamentos"""
        filter_frame = ttk.Frame(parent, style='Card.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título dos filtros
        ttk.Label(filter_frame, text="Filtros", style='Title.TLabel').pack(pady=5)
        
        # Frame dos filtros
        filters_content = ttk.Frame(filter_frame)
        filters_content.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Data
        ttk.Label(filters_content, text="Data:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.data_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.data_entry = ttk.Entry(filters_content, textvariable=self.data_var, width=12, font=('Arial', 10))
        self.data_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Status
        ttk.Label(filters_content, text="Status:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.status_combo = ttk.Combobox(filters_content, width=15, font=('Arial', 10), state='readonly')
        self.status_combo['values'] = ('Todos', 'Agendado', 'Confirmado', 'Em Andamento', 'Concluído', 'Cancelado')
        self.status_combo.set('Todos')
        self.status_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Funcionário
        ttk.Label(filters_content, text="Funcionário:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10), pady=5)
        self.funcionario_combo = ttk.Combobox(filters_content, width=20, font=('Arial', 10), state='readonly')
        self.funcionario_combo['values'] = ['Todos'] + [f.nome for f in self.funcionarios if f.ativo]
        self.funcionario_combo.set('Todos')
        self.funcionario_combo.grid(row=0, column=5, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Botões
        button_frame = ttk.Frame(filters_content)
        button_frame.grid(row=0, column=6, sticky=tk.W, padx=(20, 0), pady=5)
        
        ttk.Button(
            button_frame, 
            text="Filtrar", 
            command=self.apply_filters,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Limpar", 
            command=self.clear_filters,
            style='Action.TButton'
        ).pack(side=tk.LEFT)
    
    def create_agendamentos_list(self, parent):
        """Cria a lista de agendamentos"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Agendamentos", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Atualizar", 
            command=self.refresh_agendamentos_list,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Novo Agendamento", 
            command=self.new_agendamento,
            style='Action.TButton'
        ).pack(side=tk.LEFT)
        
        # Treeview para lista de agendamentos
        columns = ('Data', 'Hora', 'Cliente', 'Funcionário', 'Serviço', 'Status', 'Valor')
        self.agendamentos_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=20)
        
        # Configurar colunas
        self.agendamentos_tree.heading('Data', text='Data')
        self.agendamentos_tree.heading('Hora', text='Hora')
        self.agendamentos_tree.heading('Cliente', text='Cliente')
        self.agendamentos_tree.heading('Funcionário', text='Funcionário')
        self.agendamentos_tree.heading('Serviço', text='Serviço')
        self.agendamentos_tree.heading('Status', text='Status')
        self.agendamentos_tree.heading('Valor', text='Valor')
        
        self.agendamentos_tree.column('Data', width=100)
        self.agendamentos_tree.column('Hora', width=80)
        self.agendamentos_tree.column('Cliente', width=150)
        self.agendamentos_tree.column('Funcionário', width=150)
        self.agendamentos_tree.column('Serviço', width=200)
        self.agendamentos_tree.column('Status', width=120)
        self.agendamentos_tree.column('Valor', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.agendamentos_tree.yview)
        self.agendamentos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.agendamentos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind duplo clique
        self.agendamentos_tree.bind('<Double-1>', self.on_agendamento_double_click)
    
    def load_sample_data(self):
        """Carrega dados de exemplo"""
        # Clientes
        self.clientes = [
            Cliente(1, "João Silva", "(11) 99999-9999", "joao@email.com", datetime.now(), "Cliente VIP", True),
            Cliente(2, "Maria Santos", "(11) 88888-8888", "maria@email.com", datetime.now(), "", True),
            Cliente(3, "Pedro Oliveira", "(11) 77777-7777", "pedro@email.com", datetime.now(), "Prefere corte tradicional", True),
        ]
        
        # Funcionários
        self.funcionarios = [
            Funcionario(1, "Carlos Silva", "(11) 99999-9999", "carlos@barbearia.com", "Barbeiro", datetime.now(), 2500.00, True),
            Funcionario(2, "Maria Santos", "(11) 88888-8888", "maria@barbearia.com", "Barbeira", datetime.now(), 2500.00, True),
        ]
        
        # Serviços
        self.servicos = [
            Servico(1, "Corte Masculino", "Corte de cabelo masculino tradicional", 25.00, 30, True),
            Servico(2, "Barba", "Aparar e modelar barba", 15.00, 20, True),
            Servico(3, "Corte + Barba", "Corte de cabelo + barba", 35.00, 45, True),
        ]
        
        # Agendamentos
        hoje = datetime.now().date()
        self.agendamentos = [
            Agendamento(1, 1, 1, 1, hoje, datetime.combine(hoje, datetime.min.time().replace(hour=9)), datetime.combine(hoje, datetime.min.time().replace(hour=9, minute=30)), "confirmado", "", 25.00),
            Agendamento(2, 2, 2, 2, hoje, datetime.combine(hoje, datetime.min.time().replace(hour=10)), datetime.combine(hoje, datetime.min.time().replace(hour=10, minute=20)), "agendado", "", 15.00),
            Agendamento(3, 3, 1, 3, hoje, datetime.combine(hoje, datetime.min.time().replace(hour=14)), datetime.combine(hoje, datetime.min.time().replace(hour=14, minute=45)), "em_andamento", "", 35.00),
            Agendamento(4, 1, 2, 1, hoje + timedelta(days=1), datetime.combine(hoje + timedelta(days=1), datetime.min.time().replace(hour=9)), datetime.combine(hoje + timedelta(days=1), datetime.min.time().replace(hour=9, minute=30)), "agendado", "", 25.00),
        ]
    
    def refresh_agendamentos_list(self):
        """Atualiza a lista de agendamentos"""
        # Limpar lista
        for item in self.agendamentos_tree.get_children():
            self.agendamentos_tree.delete(item)
        
        # Aplicar filtros
        filtered_agendamentos = self.get_filtered_agendamentos()
        
        # Adicionar agendamentos
        for agendamento in filtered_agendamentos:
            cliente = next((c for c in self.clientes if c.id == agendamento.cliente_id), None)
            funcionario = next((f for f in self.funcionarios if f.id == agendamento.funcionario_id), None)
            servico = next((s for s in self.servicos if s.id == agendamento.servico_id), None)
            
            if cliente and funcionario and servico:
                data_str = agendamento.data_agendamento.strftime("%d/%m/%Y") if agendamento.data_agendamento else ""
                hora_str = agendamento.horario_inicio.strftime("%H:%M") if agendamento.horario_inicio else ""
                status_str = agendamento.status.replace('_', ' ').title()
                valor_str = f"R$ {agendamento.valor_total:.2f}"
                
                item = self.agendamentos_tree.insert('', 'end', values=(
                    data_str,
                    hora_str,
                    cliente.nome,
                    funcionario.nome,
                    servico.nome,
                    status_str,
                    valor_str
                ), tags=(agendamento.id,))
                
                # Aplicar cor baseada no status
                if agendamento.status == 'agendado':
                    self.agendamentos_tree.set(item, 'Status', 'Agendado')
                elif agendamento.status == 'confirmado':
                    self.agendamentos_tree.set(item, 'Status', 'Confirmado')
                elif agendamento.status == 'em_andamento':
                    self.agendamentos_tree.set(item, 'Status', 'Em Andamento')
                elif agendamento.status == 'concluido':
                    self.agendamentos_tree.set(item, 'Status', 'Concluído')
                elif agendamento.status == 'cancelado':
                    self.agendamentos_tree.set(item, 'Status', 'Cancelado')
    
    def get_filtered_agendamentos(self):
        """Retorna agendamentos filtrados"""
        filtered = self.agendamentos.copy()
        
        # Filtro por data
        try:
            data_filtro = datetime.strptime(self.data_var.get(), "%d/%m/%Y").date()
            filtered_agendamentos = []
            for a in filtered:
                if not a.data_agendamento:
                    continue
                
                # Normalizar data_agendamento para date
                try:
                    if isinstance(a.data_agendamento, datetime):
                        data_agendamento_date = a.data_agendamento.date()
                    elif isinstance(a.data_agendamento, date):
                        data_agendamento_date = a.data_agendamento
                    else:
                        continue
                    
                    # Comparar apenas se ambos forem date
                    if isinstance(data_agendamento_date, date) and isinstance(data_filtro, date):
                        if data_agendamento_date == data_filtro:
                            filtered_agendamentos.append(a)
                except (AttributeError, TypeError, ValueError):
                    continue
            
            filtered = filtered_agendamentos
        except ValueError:
            pass  # Se data inválida, não filtrar por data
        
        # Filtro por status
        status_filtro = self.status_combo.get()
        if status_filtro != 'Todos':
            status_map = {
                'Agendado': 'agendado',
                'Confirmado': 'confirmado',
                'Em Andamento': 'em_andamento',
                'Concluído': 'concluido',
                'Cancelado': 'cancelado'
            }
            if status_filtro in status_map:
                filtered = [a for a in filtered if a.status == status_map[status_filtro]]
        
        # Filtro por funcionário
        funcionario_filtro = self.funcionario_combo.get()
        if funcionario_filtro != 'Todos':
            funcionario = next((f for f in self.funcionarios if f.nome == funcionario_filtro), None)
            if funcionario:
                filtered = [a for a in filtered if a.funcionario_id == funcionario.id]
        
        return filtered
    
    def apply_filters(self):
        """Aplica os filtros"""
        self.refresh_agendamentos_list()
    
    def clear_filters(self):
        """Limpa os filtros"""
        self.data_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.status_combo.set('Todos')
        self.funcionario_combo.set('Todos')
        self.refresh_agendamentos_list()
    
    def on_agendamento_double_click(self, event):
        """Callback quando um agendamento é clicado duas vezes"""
        selection = self.agendamentos_tree.selection()
        if selection:
            item = self.agendamentos_tree.item(selection[0])
            agendamento_id = item['tags'][0] if item['tags'] else None
            
            if agendamento_id:
                agendamento = next((a for a in self.agendamentos if a.id == agendamento_id), None)
                if agendamento:
                    self.show_agendamento_details(agendamento)
    
    def show_agendamento_details(self, agendamento: Agendamento):
        """Mostra detalhes do agendamento"""
        cliente = next((c for c in self.clientes if c.id == agendamento.cliente_id), None)
        funcionario = next((f for f in self.funcionarios if f.id == agendamento.funcionario_id), None)
        servico = next((s for s in self.servicos if s.id == agendamento.servico_id), None)
        
        if cliente and funcionario and servico:
            details = f"""
Detalhes do Agendamento:

ID: {agendamento.id}
Cliente: {cliente.nome} ({cliente.telefone})
Funcionário: {funcionario.nome} ({funcionario.cargo})
Serviço: {servico.nome}
Data: {agendamento.data_agendamento.strftime('%d/%m/%Y') if agendamento.data_agendamento else 'N/A'}
Horário: {agendamento.horario_inicio.strftime('%H:%M') if agendamento.horario_inicio else 'N/A'}
Status: {agendamento.status.replace('_', ' ').title()}
Valor: R$ {agendamento.valor_total:.2f}
Observações: {agendamento.observacoes or 'Nenhuma'}
            """
            messagebox.showinfo("Detalhes do Agendamento", details)
    
    def new_agendamento(self):
        """Cria um novo agendamento"""
        messagebox.showinfo("Info", "Funcionalidade de novo agendamento será implementada em breve.")
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()


class AgendamentosWidget:
    """Widget de visualização de agendamentos para uso embutido"""
    
    def __init__(self, parent):
        self.parent = parent
        self.agendamentos: List[Agendamento] = []
        self.clientes: List[Cliente] = []
        self.funcionarios: List[Funcionario] = []
        self.servicos: List[Servico] = []
        self.data_manager = get_data_manager()
        self.create_widget()
        self.load_data_from_files()
    
    def create_widget(self):
        """Cria o widget de agendamentos"""
        # Frame principal do widget
        self.main_frame = ttk.Frame(self.parent)
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Configurar estilo
        style = ttk.Style()
        style.theme_use('clam')
        self.configure_styles(style)
        
        # Criar layout
        self.create_layout()
    
    def configure_styles(self, style):
        """Configura os estilos da interface"""
        style.configure('Card.TFrame', background='white', relief='solid', borderwidth=1)
        style.configure('Title.TLabel', font=('Arial', 14, 'bold'), background='white')
        style.configure('Subtitle.TLabel', font=('Arial', 10), background='white', foreground='#666')
        style.configure('Action.TButton', padding=(8, 4))
        
        # Estilos para status
        style.configure('Agendado.TLabel', foreground='#0078d4')
        style.configure('Confirmado.TLabel', foreground='#107c10')
        style.configure('EmAndamento.TLabel', foreground='#ff8c00')
        style.configure('Concluido.TLabel', foreground='#107c10')
        style.configure('Cancelado.TLabel', foreground='#d13438')
    
    def create_layout(self):
        """Cria o layout principal"""
        # Filtros
        self.create_filters()
        
        # Lista de agendamentos
        self.create_agendamentos_list()
    
    def create_filters(self):
        """Cria os filtros de agendamentos"""
        filter_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título dos filtros
        ttk.Label(filter_frame, text="Filtros", style='Title.TLabel').pack(pady=10)
        
        # Frame dos filtros
        filters_content = ttk.Frame(filter_frame)
        filters_content.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Data
        ttk.Label(filters_content, text="Data:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.data_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.data_entry = ttk.Entry(filters_content, textvariable=self.data_var, width=12, font=('Arial', 10))
        self.data_entry.grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Status
        ttk.Label(filters_content, text="Status:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.status_combo = ttk.Combobox(filters_content, width=15, font=('Arial', 10), state='readonly')
        self.status_combo['values'] = ('Todos', 'Agendado', 'Confirmado', 'Em Andamento', 'Concluído', 'Cancelado')
        self.status_combo.set('Todos')
        self.status_combo.grid(row=0, column=3, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Botões
        button_frame = ttk.Frame(filters_content)
        button_frame.grid(row=0, column=4, sticky=tk.W, padx=(20, 0), pady=5)
        
        ttk.Button(
            button_frame, 
            text="Filtrar", 
            command=self.apply_filters,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Limpar", 
            command=self.clear_filters,
            style='Action.TButton'
        ).pack(side=tk.LEFT)
    
    def create_agendamentos_list(self):
        """Cria a lista de agendamentos"""
        list_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Agendamentos", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Atualizar", 
            command=self.refresh_agendamentos_list,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Editar", 
            command=self.edit_agendamento,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            action_frame, 
            text="Novo Agendamento", 
            command=self.new_agendamento,
            style='Action.TButton'
        ).pack(side=tk.LEFT)
        
        # Treeview para lista de agendamentos
        columns = ('Data', 'Hora', 'Cliente', 'Funcionário', 'Serviço', 'Status', 'Valor')
        self.agendamentos_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.agendamentos_tree.heading('Data', text='Data')
        self.agendamentos_tree.heading('Hora', text='Hora')
        self.agendamentos_tree.heading('Cliente', text='Cliente')
        self.agendamentos_tree.heading('Funcionário', text='Funcionário')
        self.agendamentos_tree.heading('Serviço', text='Serviço')
        self.agendamentos_tree.heading('Status', text='Status')
        self.agendamentos_tree.heading('Valor', text='Valor')
        
        self.agendamentos_tree.column('Data', width=80)
        self.agendamentos_tree.column('Hora', width=60)
        self.agendamentos_tree.column('Cliente', width=120)
        self.agendamentos_tree.column('Funcionário', width=120)
        self.agendamentos_tree.column('Serviço', width=150)
        self.agendamentos_tree.column('Status', width=100)
        self.agendamentos_tree.column('Valor', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.agendamentos_tree.yview)
        self.agendamentos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.agendamentos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind duplo clique
        self.agendamentos_tree.bind('<Double-1>', self.on_agendamento_double_click)
    
    def load_data_from_files(self):
        """Carrega dados dos arquivos usando threads"""
        def on_clientes_loaded(clientes):
            self.clientes = clientes
            check_all_loaded()
        
        def on_funcionarios_loaded(funcionarios):
            self.funcionarios = funcionarios
            check_all_loaded()
        
        def on_servicos_loaded(servicos):
            self.servicos = servicos
            check_all_loaded()
        
        def on_agendamentos_loaded(agendamentos):
            self.agendamentos = agendamentos
            check_all_loaded()
        
        loaded_count = [0]
        def check_all_loaded():
            loaded_count[0] += 1
            if loaded_count[0] == 4:
                self.refresh_agendamentos_list()
        
        # Força recarregamento dos dados do arquivo
        self.data_manager.load_clientes(on_clientes_loaded)
        self.data_manager.load_funcionarios(on_funcionarios_loaded)
        self.data_manager.load_servicos(on_servicos_loaded)
        self.data_manager.load_agendamentos(on_agendamentos_loaded, force_reload=True)
    
    def refresh_agendamentos_list(self):
        """Atualiza a lista de agendamentos"""
        # Limpar lista
        for item in self.agendamentos_tree.get_children():
            self.agendamentos_tree.delete(item)
        
        # Aplicar filtros
        filtered_agendamentos = self.get_filtered_agendamentos()
        
        # Adicionar agendamentos
        for agendamento in filtered_agendamentos:
            cliente = next((c for c in self.clientes if c.id == agendamento.cliente_id), None)
            funcionario = next((f for f in self.funcionarios if f.id == agendamento.funcionario_id), None)
            servico = next((s for s in self.servicos if s.id == agendamento.servico_id), None)
            
            if cliente and funcionario and servico:
                data_str = agendamento.data_agendamento.strftime("%d/%m/%Y") if agendamento.data_agendamento else ""
                hora_str = agendamento.horario_inicio.strftime("%H:%M") if agendamento.horario_inicio else ""
                status_str = agendamento.status.replace('_', ' ').title()
                valor_str = f"R$ {agendamento.valor_total:.2f}"
                
                item = self.agendamentos_tree.insert('', 'end', values=(
                    data_str,
                    hora_str,
                    cliente.nome,
                    funcionario.nome,
                    servico.nome,
                    status_str,
                    valor_str
                ), tags=(agendamento.id,))
    
    def get_filtered_agendamentos(self):
        """Retorna agendamentos filtrados"""
        filtered = self.agendamentos.copy()
        
        # Filtro por data
        try:
            data_filtro = datetime.strptime(self.data_var.get(), "%d/%m/%Y").date()
            filtered_agendamentos = []
            for a in filtered:
                if not a.data_agendamento:
                    continue
                
                # Normalizar data_agendamento para date
                try:
                    if isinstance(a.data_agendamento, datetime):
                        data_agendamento_date = a.data_agendamento.date()
                    elif isinstance(a.data_agendamento, date):
                        data_agendamento_date = a.data_agendamento
                    else:
                        continue
                    
                    # Comparar apenas se ambos forem date
                    if isinstance(data_agendamento_date, date) and isinstance(data_filtro, date):
                        if data_agendamento_date == data_filtro:
                            filtered_agendamentos.append(a)
                except (AttributeError, TypeError, ValueError):
                    continue
            
            filtered = filtered_agendamentos
        except ValueError:
            pass  # Se data inválida, não filtrar por data
        
        # Filtro por status
        status_filtro = self.status_combo.get()
        if status_filtro != 'Todos':
            status_map = {
                'Agendado': 'agendado',
                'Confirmado': 'confirmado',
                'Em Andamento': 'em_andamento',
                'Concluído': 'concluido',
                'Cancelado': 'cancelado'
            }
            if status_filtro in status_map:
                filtered = [a for a in filtered if a.status == status_map[status_filtro]]
        
        return filtered
    
    def apply_filters(self):
        """Aplica os filtros"""
        self.refresh_agendamentos_list()
    
    def clear_filters(self):
        """Limpa os filtros"""
        self.data_var.set(datetime.now().strftime("%d/%m/%Y"))
        self.status_combo.set('Todos')
        self.refresh_agendamentos_list()
    
    def on_agendamento_double_click(self, event):
        """Callback quando um agendamento é clicado duas vezes"""
        selection = self.agendamentos_tree.selection()
        if selection:
            item = self.agendamentos_tree.item(selection[0])
            agendamento_id = item['tags'][0] if item['tags'] else None
            
            if agendamento_id:
                agendamento = next((a for a in self.agendamentos if a.id == agendamento_id), None)
                if agendamento:
                    self.show_agendamento_details(agendamento)
    
    def show_agendamento_details(self, agendamento: Agendamento):
        """Mostra detalhes do agendamento"""
        cliente = next((c for c in self.clientes if c.id == agendamento.cliente_id), None)
        funcionario = next((f for f in self.funcionarios if f.id == agendamento.funcionario_id), None)
        servico = next((s for s in self.servicos if s.id == agendamento.servico_id), None)
        
        if cliente and funcionario and servico:
            details = f"""
Detalhes do Agendamento:

ID: {agendamento.id}
Cliente: {cliente.nome} ({cliente.telefone})
Funcionário: {funcionario.nome} ({funcionario.cargo})
Serviço: {servico.nome}
Data: {agendamento.data_agendamento.strftime('%d/%m/%Y') if agendamento.data_agendamento else 'N/A'}
Horário: {agendamento.horario_inicio.strftime('%H:%M') if agendamento.horario_inicio else 'N/A'}
Status: {agendamento.status.replace('_', ' ').title()}
Valor: R$ {agendamento.valor_total:.2f}
Observações: {agendamento.observacoes or 'Nenhuma'}
            """
            messagebox.showinfo("Detalhes do Agendamento", details)
    
    def new_agendamento(self):
        """Cria um novo agendamento"""
        dialog = NovoAgendamentoDialog(
            self.parent,
            self.clientes,
            self.funcionarios,
            self.servicos,
            self.agendamentos,
            self.on_agendamento_created
        )
    
    def on_agendamento_created(self, agendamento: Agendamento):
        """Callback quando um novo agendamento é criado"""
        # Adicionar novo agendamento à lista
        if not self.agendamentos:
            agendamento.id = 1
        else:
            max_id = max((a.id for a in self.agendamentos if a.id), default=0)
            agendamento.id = max_id + 1
        
        self.agendamentos.append(agendamento)
        
        # Salvar agendamentos
        def on_save_complete(success):
            if success:
                self.refresh_agendamentos_list()
                messagebox.showinfo("Sucesso", "Agendamento criado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar agendamento.")
        
        self.data_manager.save_agendamentos(self.agendamentos, on_save_complete)
    
    def edit_agendamento(self):
        """Edita um agendamento selecionado"""
        selection = self.agendamentos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um agendamento para editar.")
            return
        
        item = self.agendamentos_tree.item(selection[0])
        agendamento_id = item['tags'][0] if item['tags'] else None
        
        if not agendamento_id:
            messagebox.showerror("Erro", "Não foi possível identificar o agendamento.")
            return
        
        agendamento = next((a for a in self.agendamentos if a.id == agendamento_id), None)
        if not agendamento:
            messagebox.showerror("Erro", "Agendamento não encontrado.")
            return
        
        dialog = EditarAgendamentoDialog(
            self.parent,
            agendamento,
            self.clientes,
            self.funcionarios,
            self.servicos,
            self.agendamentos,
            self.on_agendamento_updated
        )
    
    def on_agendamento_updated(self, agendamento_atualizado: Agendamento):
        """Callback quando um agendamento é atualizado"""
        # Encontrar e atualizar o agendamento na lista
        for i, agendamento in enumerate(self.agendamentos):
            if agendamento.id == agendamento_atualizado.id:
                self.agendamentos[i] = agendamento_atualizado
                break
        
        # Salvar agendamentos
        def on_save_complete(success):
            if success:
                self.refresh_agendamentos_list()
                messagebox.showinfo("Sucesso", "Agendamento atualizado com sucesso!")
            else:
                messagebox.showerror("Erro", "Erro ao salvar agendamento.")
        
        self.data_manager.save_agendamentos(self.agendamentos, on_save_complete)


class NovoAgendamentoDialog:
    """Diálogo para criar novo agendamento com validações"""
    
    def __init__(self, parent, clientes: List[Cliente], funcionarios: List[Funcionario], 
                 servicos: List[Servico], agendamentos: List[Agendamento], 
                 callback: Optional[Callable[[Agendamento], None]] = None):
        self.parent = parent
        self.clientes = clientes
        self.funcionarios = funcionarios
        self.servicos = servicos
        self.agendamentos = agendamentos
        self.callback = callback
        self.result = None
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Novo Agendamento")
        self.dialog.geometry("500x600")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        self.center_dialog()
    
    def center_dialog(self):
        """Centraliza o diálogo na tela"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Cria os widgets do diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cliente
        ttk.Label(main_frame, text="Cliente *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.cliente_var = tk.StringVar()
        clientes_ativos = [f"{c.nome} (ID: {c.id})" for c in self.clientes if c.ativo]
        self.cliente_combo = ttk.Combobox(main_frame, textvariable=self.cliente_var, 
                                          values=clientes_ativos, state='readonly', width=40)
        self.cliente_combo.grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Funcionário
        ttk.Label(main_frame, text="Barbeiro *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.funcionario_var = tk.StringVar()
        funcionarios_ativos = [f"{f.nome} (ID: {f.id})" for f in self.funcionarios if f.ativo]
        self.funcionario_combo = ttk.Combobox(main_frame, textvariable=self.funcionario_var,
                                              values=funcionarios_ativos, state='readonly', width=40)
        self.funcionario_combo.grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.funcionario_combo.bind('<<ComboboxSelected>>', self.on_funcionario_selected)
        
        # Serviço
        ttk.Label(main_frame, text="Serviço *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.servico_var = tk.StringVar()
        servicos_ativos = [f"{s.nome} - R$ {s.preco:.2f} ({s.duracao_minutos}min)" 
                          for s in self.servicos if s.ativo]
        self.servico_combo = ttk.Combobox(main_frame, textvariable=self.servico_var,
                                         values=servicos_ativos, state='readonly', width=40)
        self.servico_combo.grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.servico_combo.bind('<<ComboboxSelected>>', self.on_servico_selected)
        
        # Data
        ttk.Label(main_frame, text="Data *:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.data_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.data_entry = ttk.Entry(main_frame, textvariable=self.data_var, width=20)
        self.data_entry.grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.data_var.trace('w', lambda *args: self.update_horarios_disponiveis())
        ttk.Label(main_frame, text="(DD/MM/AAAA)").grid(row=3, column=2, sticky=tk.W, padx=(5, 0))
        
        # Hora
        ttk.Label(main_frame, text="Hora *:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.hora_var = tk.StringVar(value="09:00")
        self.hora_entry = ttk.Entry(main_frame, textvariable=self.hora_var, width=20)
        self.hora_entry.grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        ttk.Label(main_frame, text="(HH:MM)").grid(row=4, column=2, sticky=tk.W, padx=(5, 0))
        
        # Duração (calculada automaticamente)
        ttk.Label(main_frame, text="Duração:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.duracao_label = ttk.Label(main_frame, text="0 minutos")
        self.duracao_label.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Horários disponíveis
        ttk.Label(main_frame, text="Horários Disponíveis:").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.horarios_frame = ttk.Frame(main_frame)
        self.horarios_frame.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        self.horarios_listbox = tk.Listbox(self.horarios_frame, height=5, width=30)
        self.horarios_listbox.pack(side=tk.LEFT, fill=tk.BOTH)
        scrollbar_horarios = ttk.Scrollbar(self.horarios_frame, orient=tk.VERTICAL, 
                                           command=self.horarios_listbox.yview)
        scrollbar_horarios.pack(side=tk.RIGHT, fill=tk.Y)
        self.horarios_listbox.config(yscrollcommand=scrollbar_horarios.set)
        self.horarios_listbox.bind('<<ListboxSelect>>', self.on_horario_selected)
        
        # Observações
        ttk.Label(main_frame, text="Observações:").grid(row=7, column=0, sticky=tk.NW, pady=5)
        self.observacoes_text = tk.Text(main_frame, width=40, height=5)
        self.observacoes_text.grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Valor
        ttk.Label(main_frame, text="Valor:").grid(row=8, column=0, sticky=tk.W, pady=5)
        self.valor_label = ttk.Label(main_frame, text="R$ 0,00", font=('Arial', 10, 'bold'))
        self.valor_label.grid(row=8, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=9, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Salvar", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT, padx=5)
    
    def on_funcionario_selected(self, event=None):
        """Callback quando um funcionário é selecionado"""
        self.update_horarios_disponiveis()
    
    def on_servico_selected(self, event=None):
        """Callback quando um serviço é selecionado"""
        servico_selecionado = self.servico_var.get()
        if servico_selecionado:
            # Extrair nome do serviço
            servico_nome = servico_selecionado.split(" - ")[0]
            servico = next((s for s in self.servicos if s.nome == servico_nome and s.ativo), None)
            if servico:
                self.duracao_label.config(text=f"{servico.duracao_minutos} minutos")
                self.valor_label.config(text=f"R$ {servico.preco:.2f}")
                # Atualizar horários disponíveis considerando a duração do serviço
                self.update_horarios_disponiveis()
    
    def on_horario_selected(self, event=None):
        """Callback quando um horário disponível é selecionado"""
        selection = self.horarios_listbox.curselection()
        if selection:
            horario_str = self.horarios_listbox.get(selection[0])
            self.hora_var.set(horario_str)
    
    def update_horarios_disponiveis(self):
        """Atualiza a lista de horários disponíveis para o funcionário selecionado"""
        self.horarios_listbox.delete(0, tk.END)
        
        funcionario_selecionado = self.funcionario_var.get()
        if not funcionario_selecionado:
            return
        
        # Extrair ID do funcionário
        try:
            funcionario_id = int(funcionario_selecionado.split("ID: ")[1].rstrip(")"))
        except (IndexError, ValueError):
            return
        
        # Obter data selecionada
        try:
            data_str = self.data_var.get()
            data_agendamento = datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            return
        
        # Obter agendamentos existentes do funcionário na data
        agendamentos_funcionario = []
        for a in self.agendamentos:
            if a.funcionario_id != funcionario_id:
                continue
            if a.status in ['cancelado', 'concluido']:
                continue
            
            # Normalizar data_agendamento para date
            if not a.data_agendamento:
                continue
            
            try:
                if isinstance(a.data_agendamento, datetime):
                    data_agendamento_date = a.data_agendamento.date()
                elif isinstance(a.data_agendamento, date):
                    data_agendamento_date = a.data_agendamento
                else:
                    continue
                
                # Comparar apenas se ambos forem date
                if isinstance(data_agendamento_date, date) and isinstance(data_agendamento, date):
                    if data_agendamento_date == data_agendamento:
                        agendamentos_funcionario.append(a)
            except (AttributeError, TypeError, ValueError):
                continue
        
        # Obter serviço selecionado para calcular duração
        servico_selecionado = self.servico_var.get()
        duracao_minutos = 30  # padrão
        if servico_selecionado:
            try:
                servico_nome = servico_selecionado.split(" - ")[0]
                servico = next((s for s in self.servicos if s.nome == servico_nome and s.ativo), None)
                if servico:
                    duracao_minutos = servico.duracao_minutos
            except:
                pass
        
        # Horário de funcionamento (8h às 18h)
        hora_inicio = 8
        hora_fim = 18
        
        # Gerar horários disponíveis
        horarios_disponiveis = []
        for hora in range(hora_inicio, hora_fim):
            for minuto in [0, 30]:
                horario = datetime.combine(data_agendamento, datetime.min.time().replace(hour=hora, minute=minuto))
                horario_fim_sugerido = horario + timedelta(minutes=duracao_minutos)
                
                # Verificar se o horário de término está dentro do horário de funcionamento
                if horario_fim_sugerido.hour > hora_fim or (horario_fim_sugerido.hour == hora_fim and horario_fim_sugerido.minute > 0):
                    continue
                
                # Verificar se há conflito
                conflito = False
                for agendamento in agendamentos_funcionario:
                    if agendamento.horario_inicio and agendamento.horario_fim:
                        # Verificar sobreposição
                        if (horario < agendamento.horario_fim and horario_fim_sugerido > agendamento.horario_inicio):
                            conflito = True
                            break
                
                if not conflito:
                    horarios_disponiveis.append(horario.strftime("%H:%M"))
        
        # Adicionar à lista
        for horario in horarios_disponiveis:
            self.horarios_listbox.insert(tk.END, horario)
    
    def validate(self) -> Tuple[bool, str]:
        """Valida os dados do formulário"""
        # Validar cliente
        cliente_selecionado = self.cliente_var.get()
        if not cliente_selecionado:
            return False, "Selecione um cliente."
        
        try:
            cliente_id = int(cliente_selecionado.split("ID: ")[1].rstrip(")"))
        except (IndexError, ValueError):
            return False, "Cliente inválido."
        
        cliente = next((c for c in self.clientes if c.id == cliente_id and c.ativo), None)
        if not cliente:
            return False, "Cliente não encontrado ou inativo."
        
        # Validar funcionário
        funcionario_selecionado = self.funcionario_var.get()
        if not funcionario_selecionado:
            return False, "Selecione um barbeiro."
        
        try:
            funcionario_id = int(funcionario_selecionado.split("ID: ")[1].rstrip(")"))
        except (IndexError, ValueError):
            return False, "Barbeiro inválido."
        
        funcionario = next((f for f in self.funcionarios if f.id == funcionario_id and f.ativo), None)
        if not funcionario:
            return False, "Barbeiro não encontrado ou inativo."
        
        # Validar serviço
        servico_selecionado = self.servico_var.get()
        if not servico_selecionado:
            return False, "Selecione um serviço."
        
        servico_nome = servico_selecionado.split(" - ")[0]
        servico = next((s for s in self.servicos if s.nome == servico_nome and s.ativo), None)
        if not servico:
            return False, "Serviço não encontrado ou inativo."
        
        # Validar data
        try:
            data_str = self.data_var.get()
            data_agendamento = datetime.strptime(data_str, "%d/%m/%Y").date()
        except ValueError:
            return False, "Data inválida. Use o formato DD/MM/AAAA."
        
        # Validar que a data não é no passado
        if data_agendamento < datetime.now().date():
            return False, "Não é possível agendar em datas passadas."
        
        # Validar hora
        try:
            hora_str = self.hora_var.get()
            hora_parts = hora_str.split(":")
            hora = int(hora_parts[0])
            minuto = int(hora_parts[1])
            if hora < 0 or hora > 23 or minuto < 0 or minuto > 59:
                return False, "Hora inválida."
        except (ValueError, IndexError):
            return False, "Hora inválida. Use o formato HH:MM."
        
        # Criar datetime completo
        horario_inicio = datetime.combine(data_agendamento, datetime.min.time().replace(hour=hora, minute=minuto))
        horario_fim = horario_inicio + timedelta(minutes=servico.duracao_minutos)
        
        # Validar horário de funcionamento (8h às 18h)
        if horario_inicio.hour < 8 or horario_fim.hour > 18 or (horario_fim.hour == 18 and horario_fim.minute > 0):
            return False, "Horário fora do horário de funcionamento (8h às 18h)."
        
        # Validar conflito de horário
        agendamentos_funcionario = []
        for a in self.agendamentos:
            if a.funcionario_id != funcionario_id:
                continue
            if a.status in ['cancelado', 'concluido']:
                continue
            
            # Normalizar data_agendamento para date
            if not a.data_agendamento:
                continue
            
            try:
                if isinstance(a.data_agendamento, datetime):
                    data_agendamento_date = a.data_agendamento.date()
                elif isinstance(a.data_agendamento, date):
                    data_agendamento_date = a.data_agendamento
                else:
                    continue
                
                # Comparar apenas se ambos forem date
                if isinstance(data_agendamento_date, date) and isinstance(data_agendamento, date):
                    if data_agendamento_date == data_agendamento:
                        agendamentos_funcionario.append(a)
            except (AttributeError, TypeError, ValueError):
                continue
        
        for agendamento in agendamentos_funcionario:
            if agendamento.horario_inicio and agendamento.horario_fim:
                # Verificar sobreposição
                if (horario_inicio < agendamento.horario_fim and horario_fim > agendamento.horario_inicio):
                    return False, f"Conflito de horário. Barbeiro já tem agendamento das {agendamento.horario_inicio.strftime('%H:%M')} às {agendamento.horario_fim.strftime('%H:%M')}."
        
        return True, ""
    
    def save(self):
        """Salva o agendamento"""
        valid, error_msg = self.validate()
        if not valid:
            messagebox.showerror("Erro de Validação", error_msg)
            return
        
        # Extrair dados
        cliente_id = int(self.cliente_var.get().split("ID: ")[1].rstrip(")"))
        funcionario_id = int(self.funcionario_var.get().split("ID: ")[1].rstrip(")"))
        servico_nome = self.servico_var.get().split(" - ")[0]
        servico = next((s for s in self.servicos if s.nome == servico_nome), None)
        
        data_str = self.data_var.get()
        data_agendamento_date = datetime.strptime(data_str, "%d/%m/%Y").date()
        
        hora_str = self.hora_var.get()
        hora_parts = hora_str.split(":")
        hora = int(hora_parts[0])
        minuto = int(hora_parts[1])
        
        horario_inicio = datetime.combine(data_agendamento_date, datetime.min.time().replace(hour=hora, minute=minuto))
        horario_fim = horario_inicio + timedelta(minutes=servico.duracao_minutos)
        
        # data_agendamento deve ser um datetime (com hora 00:00:00)
        data_agendamento = datetime.combine(data_agendamento_date, datetime.min.time())
        
        observacoes = self.observacoes_text.get("1.0", tk.END).strip()
        
        # Criar agendamento
        agendamento = Agendamento(
            id=None,  # Será definido pelo widget
            cliente_id=cliente_id,
            funcionario_id=funcionario_id,
            servico_id=servico.id,
            data_agendamento=data_agendamento,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            status="agendado",
            observacoes=observacoes,
            valor_total=servico.preco
        )
        
        if self.callback:
            self.callback(agendamento)
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela o diálogo"""
        self.dialog.destroy()


class EditarAgendamentoDialog:
    """Diálogo para editar agendamento existente"""
    
    def __init__(self, parent, agendamento: Agendamento, clientes: List[Cliente], 
                 funcionarios: List[Funcionario], servicos: List[Servico], 
                 agendamentos: List[Agendamento], 
                 callback: Optional[Callable[[Agendamento], None]] = None):
        self.parent = parent
        self.agendamento_original = agendamento
        self.clientes = clientes
        self.funcionarios = funcionarios
        self.servicos = servicos
        self.agendamentos = agendamentos
        self.callback = callback
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Agendamento")
        self.dialog.geometry("500x650")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        self.create_widgets()
        self.load_agendamento_data()
        self.center_dialog()
    
    def center_dialog(self):
        """Centraliza o diálogo na tela"""
        self.dialog.update_idletasks()
        width = self.dialog.winfo_width()
        height = self.dialog.winfo_height()
        x = (self.dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (height // 2)
        self.dialog.geometry(f'{width}x{height}+{x}+{y}')
    
    def create_widgets(self):
        """Cria os widgets do diálogo"""
        main_frame = ttk.Frame(self.dialog, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Cliente (somente leitura)
        ttk.Label(main_frame, text="Cliente:").grid(row=0, column=0, sticky=tk.W, pady=5)
        cliente = next((c for c in self.clientes if c.id == self.agendamento_original.cliente_id), None)
        cliente_nome = cliente.nome if cliente else "Não encontrado"
        ttk.Label(main_frame, text=cliente_nome, font=('Arial', 10)).grid(row=0, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Funcionário (somente leitura)
        ttk.Label(main_frame, text="Barbeiro:").grid(row=1, column=0, sticky=tk.W, pady=5)
        funcionario = next((f for f in self.funcionarios if f.id == self.agendamento_original.funcionario_id), None)
        funcionario_nome = funcionario.nome if funcionario else "Não encontrado"
        ttk.Label(main_frame, text=funcionario_nome, font=('Arial', 10)).grid(row=1, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Serviço (somente leitura)
        ttk.Label(main_frame, text="Serviço:").grid(row=2, column=0, sticky=tk.W, pady=5)
        servico = next((s for s in self.servicos if s.id == self.agendamento_original.servico_id), None)
        servico_nome = servico.nome if servico else "Não encontrado"
        ttk.Label(main_frame, text=servico_nome, font=('Arial', 10)).grid(row=2, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Data (somente leitura)
        ttk.Label(main_frame, text="Data:").grid(row=3, column=0, sticky=tk.W, pady=5)
        data_str = self.agendamento_original.data_agendamento.strftime("%d/%m/%Y") if self.agendamento_original.data_agendamento else "N/A"
        ttk.Label(main_frame, text=data_str, font=('Arial', 10)).grid(row=3, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Hora (somente leitura)
        ttk.Label(main_frame, text="Hora:").grid(row=4, column=0, sticky=tk.W, pady=5)
        hora_str = self.agendamento_original.horario_inicio.strftime("%H:%M") if self.agendamento_original.horario_inicio else "N/A"
        ttk.Label(main_frame, text=hora_str, font=('Arial', 10)).grid(row=4, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Status (editável)
        ttk.Label(main_frame, text="Status *:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.status_var = tk.StringVar()
        self.status_combo = ttk.Combobox(main_frame, textvariable=self.status_var, width=20, state='readonly')
        self.status_combo['values'] = ('agendado', 'confirmado', 'em_andamento', 'concluido', 'cancelado')
        self.status_combo.grid(row=5, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Observações (editável)
        ttk.Label(main_frame, text="Observações:").grid(row=6, column=0, sticky=tk.NW, pady=5)
        self.observacoes_text = tk.Text(main_frame, width=40, height=8)
        self.observacoes_text.grid(row=6, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Valor (somente leitura)
        ttk.Label(main_frame, text="Valor:").grid(row=7, column=0, sticky=tk.W, pady=5)
        valor_str = f"R$ {self.agendamento_original.valor_total:.2f}"
        ttk.Label(main_frame, text=valor_str, font=('Arial', 10, 'bold')).grid(row=7, column=1, sticky=tk.W, pady=5, padx=(10, 0))
        
        # Botões
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=8, column=0, columnspan=3, pady=20)
        
        ttk.Button(button_frame, text="Salvar", command=self.save).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.cancel).pack(side=tk.LEFT, padx=5)
    
    def load_agendamento_data(self):
        """Carrega os dados do agendamento nos campos"""
        self.status_var.set(self.agendamento_original.status)
        self.observacoes_text.insert("1.0", self.agendamento_original.observacoes or "")
    
    def validate(self) -> Tuple[bool, str]:
        """Valida os dados do formulário"""
        status = self.status_var.get()
        if not status:
            return False, "Selecione um status."
        
        if status not in ['agendado', 'confirmado', 'em_andamento', 'concluido', 'cancelado']:
            return False, "Status inválido."
        
        return True, ""
    
    def save(self):
        """Salva as alterações do agendamento"""
        valid, error_msg = self.validate()
        if not valid:
            messagebox.showerror("Erro de Validação", error_msg)
            return
        
        # Atualizar agendamento
        self.agendamento_original.status = self.status_var.get()
        self.agendamento_original.observacoes = self.observacoes_text.get("1.0", tk.END).strip()
        
        if self.callback:
            self.callback(self.agendamento_original)
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela o diálogo"""
        self.dialog.destroy()