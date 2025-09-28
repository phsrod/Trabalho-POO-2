import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from models import Agendamento, Cliente, Funcionario, Servico
from datetime import datetime, timedelta

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
        ttk.Label(filter_frame, text="Filtros", style='Title.TLabel').pack(pady=15)
        
        # Frame dos filtros
        filters_content = ttk.Frame(filter_frame)
        filters_content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
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
            filtered = [a for a in filtered if a.data_agendamento == data_filtro]
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
