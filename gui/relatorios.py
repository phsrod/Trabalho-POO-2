import tkinter as tk
from tkinter import ttk, messagebox
from typing import List
from models import Cliente, Funcionario, Servico, Agendamento
from datetime import datetime, timedelta
from collections import defaultdict

class RelatoriosWindow:
    """Janela de relatórios e estatísticas"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.window = None
        self.clientes: List[Cliente] = []
        self.funcionarios: List[Funcionario] = []
        self.servicos: List[Servico] = []
        self.agendamentos: List[Agendamento] = []
        self.create_window()
        self.load_sample_data()
        self.update_statistics()
    
    def create_window(self):
        """Cria a janela de relatórios"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Relatórios e Estatísticas")
        self.window.geometry("1200x800")
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
        style.configure('Stat.TLabel', font=('Arial', 12, 'bold'), background='white', foreground='#0078d4')
        style.configure('Action.TButton', padding=(8, 4))
    
    def create_layout(self):
        """Cria o layout principal"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Relatórios e Estatísticas", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Filtros de período
        self.create_period_filters(main_frame)
        
        # Estatísticas gerais
        self.create_general_stats(main_frame)
        
        # Relatórios específicos
        self.create_specific_reports(main_frame)
    
    def create_period_filters(self, parent):
        """Cria os filtros de período"""
        filter_frame = ttk.Frame(parent, style='Card.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Título dos filtros
        ttk.Label(filter_frame, text="Filtros de Período", style='Title.TLabel').pack(pady=15)
        
        # Frame dos filtros
        filters_content = ttk.Frame(filter_frame)
        filters_content.pack(fill=tk.X, padx=20, pady=(0, 15))
        
        # Período
        ttk.Label(filters_content, text="Período:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.period_var = tk.StringVar(value="Este Mês")
        self.period_combo = ttk.Combobox(filters_content, textvariable=self.period_var, width=15, font=('Arial', 10), state='readonly')
        self.period_combo['values'] = ('Hoje', 'Esta Semana', 'Este Mês', 'Últimos 3 Meses', 'Este Ano', 'Personalizado')
        self.period_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        self.period_combo.bind('<<ComboboxSelected>>', self.on_period_change)
        
        # Data inicial
        ttk.Label(filters_content, text="Data Inicial:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.data_inicial_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.data_inicial_entry = ttk.Entry(filters_content, textvariable=self.data_inicial_var, width=12, font=('Arial', 10))
        self.data_inicial_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Data final
        ttk.Label(filters_content, text="Data Final:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10), pady=5)
        self.data_final_var = tk.StringVar(value=datetime.now().strftime("%d/%m/%Y"))
        self.data_final_entry = ttk.Entry(filters_content, textvariable=self.data_final_var, width=12, font=('Arial', 10))
        self.data_final_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Botão atualizar
        ttk.Button(
            filters_content, 
            text="Atualizar", 
            command=self.update_statistics,
            style='Action.TButton'
        ).grid(row=0, column=6, sticky=tk.W, padx=(20, 0), pady=5)
    
    def create_general_stats(self, parent):
        """Cria as estatísticas gerais"""
        stats_frame = ttk.Frame(parent)
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Card 1 - Total de Clientes
        clientes_card = ttk.Frame(stats_frame, style='Card.TFrame')
        clientes_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        ttk.Label(clientes_card, text="Total de Clientes", style='Title.TLabel').pack(pady=(15, 5))
        self.clientes_total_label = ttk.Label(clientes_card, text="0", style='Stat.TLabel')
        self.clientes_total_label.pack(pady=(0, 15))
        
        # Card 2 - Agendamentos do Período
        agendamentos_card = ttk.Frame(stats_frame, style='Card.TFrame')
        agendamentos_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(agendamentos_card, text="Agendamentos", style='Title.TLabel').pack(pady=(15, 5))
        self.agendamentos_total_label = ttk.Label(agendamentos_card, text="0", style='Stat.TLabel')
        self.agendamentos_total_label.pack(pady=(0, 15))
        
        # Card 3 - Receita Total
        receita_card = ttk.Frame(stats_frame, style='Card.TFrame')
        receita_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)
        
        ttk.Label(receita_card, text="Receita Total", style='Title.TLabel').pack(pady=(15, 5))
        self.receita_total_label = ttk.Label(receita_card, text="R$ 0,00", style='Stat.TLabel')
        self.receita_total_label.pack(pady=(0, 15))
        
        # Card 4 - Funcionários Ativos
        funcionarios_card = ttk.Frame(stats_frame, style='Card.TFrame')
        funcionarios_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        ttk.Label(funcionarios_card, text="Funcionários Ativos", style='Title.TLabel').pack(pady=(15, 5))
        self.funcionarios_total_label = ttk.Label(funcionarios_card, text="0", style='Stat.TLabel')
        self.funcionarios_total_label.pack(pady=(0, 15))
    
    def create_specific_reports(self, parent):
        """Cria os relatórios específicos"""
        reports_frame = ttk.Frame(parent)
        reports_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Relatórios
        left_frame = ttk.Frame(reports_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Relatório de Serviços Mais Populares
        self.create_services_report(left_frame)
        
        # Coluna direita - Relatórios
        right_frame = ttk.Frame(reports_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Relatório de Funcionários
        self.create_employees_report(right_frame)
    
    def create_services_report(self, parent):
        """Cria relatório de serviços"""
        services_frame = ttk.Frame(parent, style='Card.TFrame')
        services_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        ttk.Label(services_frame, text="Serviços Mais Populares", style='Title.TLabel').pack(pady=15)
        
        # Treeview para serviços
        columns = ('Serviço', 'Quantidade', 'Receita')
        self.services_tree = ttk.Treeview(services_frame, columns=columns, show='headings', height=8)
        
        self.services_tree.heading('Serviço', text='Serviço')
        self.services_tree.heading('Quantidade', text='Quantidade')
        self.services_tree.heading('Receita', text='Receita')
        
        self.services_tree.column('Serviço', width=200)
        self.services_tree.column('Quantidade', width=100)
        self.services_tree.column('Receita', width=100)
        
        self.services_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def create_employees_report(self, parent):
        """Cria relatório de funcionários"""
        employees_frame = ttk.Frame(parent, style='Card.TFrame')
        employees_frame.pack(fill=tk.BOTH, expand=True)
        
        ttk.Label(employees_frame, text="Performance dos Funcionários", style='Title.TLabel').pack(pady=15)
        
        # Treeview para funcionários
        columns = ('Funcionário', 'Agendamentos', 'Receita')
        self.employees_tree = ttk.Treeview(employees_frame, columns=columns, show='headings', height=8)
        
        self.employees_tree.heading('Funcionário', text='Funcionário')
        self.employees_tree.heading('Agendamentos', text='Agendamentos')
        self.employees_tree.heading('Receita', text='Receita')
        
        self.employees_tree.column('Funcionário', width=200)
        self.employees_tree.column('Agendamentos', width=100)
        self.employees_tree.column('Receita', width=100)
        
        self.employees_tree.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
    
    def load_sample_data(self):
        """Carrega dados de exemplo"""
        # Clientes
        self.clientes = [
            Cliente(1, "João Silva", "(11) 99999-9999", "joao@email.com", datetime.now(), "Cliente VIP", True),
            Cliente(2, "Maria Santos", "(11) 88888-8888", "maria@email.com", datetime.now(), "", True),
            Cliente(3, "Pedro Oliveira", "(11) 77777-7777", "pedro@email.com", datetime.now(), "Prefere corte tradicional", True),
            Cliente(4, "Ana Costa", "(11) 66666-6666", "ana@email.com", datetime.now(), "", False),
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
        
        # Agendamentos (últimos 30 dias)
        hoje = datetime.now().date()
        self.agendamentos = []
        
        # Gerar agendamentos de exemplo para os últimos 30 dias
        for i in range(30):
            data = hoje - timedelta(days=i)
            if i < 5:  # Apenas alguns dias com agendamentos
                for j in range(3):  # 3 agendamentos por dia
                    cliente_id = (i + j) % len(self.clientes) + 1
                    funcionario_id = (i + j) % len(self.funcionarios) + 1
                    servico_id = (i + j) % len(self.servicos) + 1
                    
                    servico = next((s for s in self.servicos if s.id == servico_id), None)
                    if servico:
                        agendamento = Agendamento(
                            id=len(self.agendamentos) + 1,
                            cliente_id=cliente_id,
                            funcionario_id=funcionario_id,
                            servico_id=servico_id,
                            data_agendamento=data,
                            horario_inicio=datetime.combine(data, datetime.min.time().replace(hour=9 + j)),
                            horario_fim=datetime.combine(data, datetime.min.time().replace(hour=9 + j, minute=30)),
                            status="concluido",
                            valor_total=servico.preco
                        )
                        self.agendamentos.append(agendamento)
    
    def on_period_change(self, event):
        """Callback quando o período é alterado"""
        period = self.period_var.get()
        hoje = datetime.now().date()
        
        if period == "Hoje":
            self.data_inicial_var.set(hoje.strftime("%d/%m/%Y"))
            self.data_final_var.set(hoje.strftime("%d/%m/%Y"))
        elif period == "Esta Semana":
            inicio_semana = hoje - timedelta(days=hoje.weekday())
            self.data_inicial_var.set(inicio_semana.strftime("%d/%m/%Y"))
            self.data_final_var.set(hoje.strftime("%d/%m/%Y"))
        elif period == "Este Mês":
            inicio_mes = hoje.replace(day=1)
            self.data_inicial_var.set(inicio_mes.strftime("%d/%m/%Y"))
            self.data_final_var.set(hoje.strftime("%d/%m/%Y"))
        elif period == "Últimos 3 Meses":
            inicio_trimestre = hoje - timedelta(days=90)
            self.data_inicial_var.set(inicio_trimestre.strftime("%d/%m/%Y"))
            self.data_final_var.set(hoje.strftime("%d/%m/%Y"))
        elif period == "Este Ano":
            inicio_ano = hoje.replace(month=1, day=1)
            self.data_inicial_var.set(inicio_ano.strftime("%d/%m/%Y"))
            self.data_final_var.set(hoje.strftime("%d/%m/%Y"))
    
    def update_statistics(self):
        """Atualiza as estatísticas"""
        try:
            # Obter período
            data_inicial = datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").date()
            data_final = datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").date()
            
            # Filtrar agendamentos do período
            agendamentos_periodo = [
                a for a in self.agendamentos 
                if a.data_agendamento and data_inicial <= a.data_agendamento <= data_final
            ]
            
            # Atualizar estatísticas gerais
            self.clientes_total_label.config(text=str(len([c for c in self.clientes if c.ativo])))
            self.agendamentos_total_label.config(text=str(len(agendamentos_periodo)))
            
            receita_total = sum(float(a.valor_total) for a in agendamentos_periodo)
            self.receita_total_label.config(text=f"R$ {receita_total:.2f}")
            
            self.funcionarios_total_label.config(text=str(len([f for f in self.funcionarios if f.ativo])))
            
            # Atualizar relatórios específicos
            self.update_services_report(agendamentos_periodo)
            self.update_employees_report(agendamentos_periodo)
            
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estatísticas: {str(e)}")
    
    def update_services_report(self, agendamentos_periodo):
        """Atualiza relatório de serviços"""
        # Limpar lista
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        # Contar serviços
        servico_count = defaultdict(int)
        servico_receita = defaultdict(float)
        
        for agendamento in agendamentos_periodo:
            servico = next((s for s in self.servicos if s.id == agendamento.servico_id), None)
            if servico:
                servico_count[servico.nome] += 1
                servico_receita[servico.nome] += float(agendamento.valor_total)
        
        # Ordenar por quantidade
        sorted_servicos = sorted(servico_count.items(), key=lambda x: x[1], reverse=True)
        
        # Adicionar à lista
        for servico_nome, quantidade in sorted_servicos:
            receita = servico_receita[servico_nome]
            self.services_tree.insert('', 'end', values=(
                servico_nome,
                quantidade,
                f"R$ {receita:.2f}"
            ))
    
    def update_employees_report(self, agendamentos_periodo):
        """Atualiza relatório de funcionários"""
        # Limpar lista
        for item in self.employees_tree.get_children():
            self.employees_tree.delete(item)
        
        # Contar funcionários
        funcionario_count = defaultdict(int)
        funcionario_receita = defaultdict(float)
        
        for agendamento in agendamentos_periodo:
            funcionario = next((f for f in self.funcionarios if f.id == agendamento.funcionario_id), None)
            if funcionario:
                funcionario_count[funcionario.nome] += 1
                funcionario_receita[funcionario.nome] += float(agendamento.valor_total)
        
        # Ordenar por quantidade
        sorted_funcionarios = sorted(funcionario_count.items(), key=lambda x: x[1], reverse=True)
        
        # Adicionar à lista
        for funcionario_nome, quantidade in sorted_funcionarios:
            receita = funcionario_receita[funcionario_nome]
            self.employees_tree.insert('', 'end', values=(
                funcionario_nome,
                quantidade,
                f"R$ {receita:.2f}"
            ))
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()
