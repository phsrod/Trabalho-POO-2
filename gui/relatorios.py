import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import List
from models import Cliente, Funcionario, Servico, Agendamento
from datetime import datetime, timedelta, date
from collections import defaultdict
from repositories import get_data_manager

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
        filters_content.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Período
        ttk.Label(filters_content, text="Período:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.period_var = tk.StringVar(value="Este Mês")
        self.period_combo = ttk.Combobox(filters_content, textvariable=self.period_var, width=15, font=('Arial', 10), state='readonly')
        self.period_combo['values'] = ('Hoje', 'Esta Semana', 'Este Mês', 'Últimos 3 Meses', 'Este Ano', 'Personalizado')
        self.period_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        self.period_combo.bind('<<ComboboxSelected>>', self.on_period_change)
        
        # Data inicial (últimos 30 dias por padrão)
        ttk.Label(filters_content, text="Data Inicial:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        data_inicial_padrao = (datetime.now() - timedelta(days=30)).strftime("%d/%m/%Y")
        self.data_inicial_var = tk.StringVar(value=data_inicial_padrao)
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
        
        # Atualizar estatísticas após mudar o período
        self.update_statistics()
    
    def update_statistics(self):
        """Atualiza as estatísticas"""
        try:
            # Obter período
            data_inicial = datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").date()
            data_final = datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").date()
            
            # Filtrar agendamentos do período (apenas concluídos para relatórios)
            agendamentos_periodo = []
            for a in self.agendamentos:
                # Verificar status
                if a.status != 'concluido':
                    continue
                
                # Verificar se tem data_agendamento
                if not a.data_agendamento:
                    continue
                
                # Converter data_agendamento para date se for datetime
                try:
                    # Normalizar data_agendamento para date
                    if isinstance(a.data_agendamento, datetime):
                        data_agendamento_date = a.data_agendamento.date()
                    elif isinstance(a.data_agendamento, date):
                        data_agendamento_date = a.data_agendamento
                    elif hasattr(a.data_agendamento, 'date') and callable(getattr(a.data_agendamento, 'date', None)):
                        data_agendamento_date = a.data_agendamento.date()
                    else:
                        # Tipo não reconhecido, pular
                        continue
                    
                    # Verificar se está no período (garantir que ambos são date)
                    if isinstance(data_agendamento_date, date) and isinstance(data_inicial, date) and isinstance(data_final, date):
                        if data_inicial <= data_agendamento_date <= data_final:
                            agendamentos_periodo.append(a)
                except (AttributeError, TypeError, ValueError) as e:
                    # Se houver erro na conversão, pular este agendamento
                    continue
            
            # Atualizar estatísticas gerais
            self.clientes_total_label.config(text=str(len([c for c in self.clientes if c.ativo])))
            self.agendamentos_total_label.config(text=str(len(agendamentos_periodo)))
            
            receita_total = sum(float(a.valor_total) for a in agendamentos_periodo)
            self.receita_total_label.config(text=f"R$ {receita_total:.2f}")
            
            self.funcionarios_total_label.config(text=str(len([f for f in self.funcionarios if f.ativo])))
            
            # Atualizar relatórios específicos
            self.update_services_report(agendamentos_periodo)
            self.update_employees_report(agendamentos_periodo)
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Formato de data inválido. Use DD/MM/AAAA\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estatísticas: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def update_services_report(self, agendamentos_periodo):
        """Atualiza relatório de serviços"""
        # Limpar lista
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        if not agendamentos_periodo:
            # Se não houver agendamentos, mostrar mensagem
            self.services_tree.insert('', 'end', values=(
                "Nenhum agendamento concluído no período",
                "0",
                "R$ 0,00"
            ))
            return
        
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
        
        if not agendamentos_periodo:
            # Se não houver agendamentos, mostrar mensagem
            self.employees_tree.insert('', 'end', values=(
                "Nenhum agendamento concluído no período",
                "0",
                "R$ 0,00"
            ))
            return
        
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
    
    def export_relatorio(self):
        """Exporta relatório em arquivo TXT usando thread"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            title="Salvar Relatório"
        )
        
        if not filename:
            return
        
        try:
            data_inicial = datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y")
            data_final = datetime.strptime(self.data_final_var.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
            return
        
        messagebox.showinfo("Exportando", "Exportando relatório em segundo plano...")
        
        def on_export_complete(success, result):
            if success:
                messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n\n{result}")
            else:
                messagebox.showerror("Erro", f"Erro ao exportar relatório:\n{result}")
        
        self.data_manager.export_relatorio_txt(
            self.clientes, self.funcionarios, self.servicos, self.agendamentos,
            data_inicial, data_final, filename, on_export_complete
        )
    
    def load_data_from_files(self):
        """Carrega dados dos arquivos usando threads"""
        from decimal import Decimal
        
        def on_clientes_loaded(clientes):
            self.clientes = clientes
            if not self.clientes:
                self.clientes = [
                    Cliente(1, "João Silva", "(11) 99999-9999", "joao@email.com", datetime.now(), "Cliente VIP", True),
                    Cliente(2, "Maria Santos", "(11) 88888-8888", "maria@email.com", datetime.now(), "", True),
                ]
            check_all_loaded()
        
        def on_funcionarios_loaded(funcionarios):
            self.funcionarios = funcionarios
            if not self.funcionarios:
                self.funcionarios = [
                    Funcionario(1, "Carlos Silva", "(11) 99999-9999", "carlos@barbearia.com", "Barbeiro", datetime.now(), 2500.00, True),
                    Funcionario(2, "Maria Santos", "(11) 88888-8888", "maria@barbearia.com", "Barbeira", datetime.now(), 2500.00, True),
                ]
            check_all_loaded()
        
        def on_servicos_loaded(servicos):
            self.servicos = servicos
            if not self.servicos:
                self.servicos = [
                    Servico(1, "Corte Masculino", "Corte de cabelo masculino tradicional", Decimal('25.00'), 30, True),
                    Servico(2, "Barba", "Aparar e modelar barba", Decimal('15.00'), 20, True),
                    Servico(3, "Corte + Barba", "Corte de cabelo + barba", Decimal('35.00'), 45, True),
                ]
            check_all_loaded()
        
        def on_agendamentos_loaded(agendamentos):
            self.agendamentos = agendamentos
            check_all_loaded()
        
        loaded_count = [0]
        def check_all_loaded():
            loaded_count[0] += 1
            if loaded_count[0] == 4:
                if not self.agendamentos:
                    hoje = datetime.now().date()
                    for i in range(30):
                        data = hoje - timedelta(days=i)
                        if i < 5:
                            for j in range(3):
                                cliente_id = (i + j) % len(self.clientes) + 1 if self.clientes else 1
                                funcionario_id = (i + j) % len(self.funcionarios) + 1 if self.funcionarios else 1
                                servico_id = (i + j) % len(self.servicos) + 1 if self.servicos else 1
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
                self.update_statistics()
        
        # Força recarregamento dos dados do arquivo
        self.data_manager.load_clientes(on_clientes_loaded)
        self.data_manager.load_funcionarios(on_funcionarios_loaded)
        self.data_manager.load_servicos(on_servicos_loaded)
        self.data_manager.load_agendamentos(on_agendamentos_loaded, force_reload=True)
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()


class RelatoriosWidget:
    """Widget de relatórios e estatísticas para uso embutido"""
    
    def __init__(self, parent, dashboard_callback=None):
        self.parent = parent
        self.clientes: List[Cliente] = []
        self.funcionarios: List[Funcionario] = []
        self.servicos: List[Servico] = []
        self.agendamentos: List[Agendamento] = []
        self.data_manager = get_data_manager()
        self.dashboard_callback = dashboard_callback  # Callback opcional (não usado aqui, mas aceito para compatibilidade)
        self.create_widget()
        self.load_data_from_files()
    
    def create_widget(self):
        """Cria o widget de relatórios"""
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
        style.configure('Stat.TLabel', font=('Arial', 12, 'bold'), background='white', foreground='#0078d4')
        style.configure('Action.TButton', padding=(8, 4))
    
    def create_layout(self):
        """Cria o layout principal"""
        # Filtros de período
        self.create_period_filters()
        
        # Estatísticas gerais
        self.create_general_stats()
        
        # Relatórios específicos
        self.create_specific_reports()
    
    def create_period_filters(self):
        """Cria os filtros de período"""
        filter_frame = ttk.Frame(self.main_frame, style='Card.TFrame')
        filter_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Título dos filtros
        ttk.Label(filter_frame, text="Filtros de Período", style='Title.TLabel').pack(pady=5)
        
        # Frame dos filtros
        filters_content = ttk.Frame(filter_frame)
        filters_content.pack(fill=tk.X, padx=5, pady=(0, 5))
        
        # Período
        ttk.Label(filters_content, text="Período:").grid(row=0, column=0, sticky=tk.W, padx=(0, 10), pady=5)
        self.period_var = tk.StringVar(value="Este Ano")
        self.period_combo = ttk.Combobox(filters_content, textvariable=self.period_var, width=15, font=('Arial', 10), state='readonly')
        self.period_combo['values'] = ('Hoje', 'Esta Semana', 'Este Mês', 'Últimos 3 Meses', 'Este Ano', 'Personalizado')
        self.period_combo.grid(row=0, column=1, sticky=tk.W, padx=(0, 20), pady=5)
        self.period_combo.bind('<<ComboboxSelected>>', self.on_period_change)
        
        # Data inicial (padrão: início do ano para incluir mais agendamentos)
        hoje = datetime.now().date()
        inicio_ano = hoje.replace(month=1, day=1)
        ttk.Label(filters_content, text="Data Inicial:").grid(row=0, column=2, sticky=tk.W, padx=(0, 10), pady=5)
        self.data_inicial_var = tk.StringVar(value=inicio_ano.strftime("%d/%m/%Y"))
        self.data_inicial_entry = ttk.Entry(filters_content, textvariable=self.data_inicial_var, width=12, font=('Arial', 10))
        self.data_inicial_entry.grid(row=0, column=3, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Data final (padrão: fim do ano)
        fim_ano = hoje.replace(month=12, day=31)
        ttk.Label(filters_content, text="Data Final:").grid(row=0, column=4, sticky=tk.W, padx=(0, 10), pady=5)
        self.data_final_var = tk.StringVar(value=fim_ano.strftime("%d/%m/%Y"))
        self.data_final_entry = ttk.Entry(filters_content, textvariable=self.data_final_var, width=12, font=('Arial', 10))
        self.data_final_entry.grid(row=0, column=5, sticky=tk.W, padx=(0, 20), pady=5)
        
        # Botão atualizar
        ttk.Button(
            filters_content, 
            text="Atualizar", 
            command=self.update_statistics,
            style='Action.TButton'
        ).grid(row=0, column=6, sticky=tk.W, padx=(20, 0), pady=5)
        
        # Botão exportar relatório
        ttk.Button(
            filters_content, 
            text="Exportar TXT", 
            command=self.export_relatorio,
            style='Action.TButton'
        ).grid(row=0, column=7, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_general_stats(self):
        """Cria as estatísticas gerais"""
        stats_frame = ttk.Frame(self.main_frame)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
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
    
    def create_specific_reports(self):
        """Cria os relatórios específicos"""
        reports_frame = ttk.Frame(self.main_frame)
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
        
        self.services_tree.column('Serviço', width=150)
        self.services_tree.column('Quantidade', width=80)
        self.services_tree.column('Receita', width=80)
        
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
        
        self.employees_tree.column('Funcionário', width=150)
        self.employees_tree.column('Agendamentos', width=80)
        self.employees_tree.column('Receita', width=80)
        
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
        
        # Atualizar estatísticas após mudar o período
        self.update_statistics()
    
    def update_statistics(self):
        """Atualiza as estatísticas"""
        try:
            # Obter período
            data_inicial = datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y").date()
            data_final = datetime.strptime(self.data_final_var.get(), "%d/%m/%Y").date()
            
            # Filtrar agendamentos do período (apenas concluídos para relatórios)
            agendamentos_periodo = []
            for a in self.agendamentos:
                # Verificar status
                if a.status != 'concluido':
                    continue
                
                # Verificar se tem data_agendamento
                if not a.data_agendamento:
                    continue
                
                # Converter data_agendamento para date se for datetime
                try:
                    # Normalizar data_agendamento para date
                    if isinstance(a.data_agendamento, datetime):
                        data_agendamento_date = a.data_agendamento.date()
                    elif isinstance(a.data_agendamento, date):
                        data_agendamento_date = a.data_agendamento
                    elif hasattr(a.data_agendamento, 'date') and callable(getattr(a.data_agendamento, 'date', None)):
                        data_agendamento_date = a.data_agendamento.date()
                    else:
                        # Tipo não reconhecido, pular
                        continue
                    
                    # Verificar se está no período (garantir que ambos são date)
                    if isinstance(data_agendamento_date, date) and isinstance(data_inicial, date) and isinstance(data_final, date):
                        if data_inicial <= data_agendamento_date <= data_final:
                            agendamentos_periodo.append(a)
                except (AttributeError, TypeError, ValueError) as e:
                    # Se houver erro na conversão, pular este agendamento
                    continue
            
            # Atualizar estatísticas gerais
            self.clientes_total_label.config(text=str(len([c for c in self.clientes if c.ativo])))
            self.agendamentos_total_label.config(text=str(len(agendamentos_periodo)))
            
            receita_total = sum(float(a.valor_total) for a in agendamentos_periodo)
            self.receita_total_label.config(text=f"R$ {receita_total:.2f}")
            
            self.funcionarios_total_label.config(text=str(len([f for f in self.funcionarios if f.ativo])))
            
            # Atualizar relatórios específicos
            self.update_services_report(agendamentos_periodo)
            self.update_employees_report(agendamentos_periodo)
            
        except ValueError as e:
            messagebox.showerror("Erro", f"Formato de data inválido. Use DD/MM/AAAA\n{str(e)}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao atualizar estatísticas: {str(e)}")
            import traceback
            traceback.print_exc()
    
    def update_services_report(self, agendamentos_periodo):
        """Atualiza relatório de serviços"""
        # Limpar lista
        for item in self.services_tree.get_children():
            self.services_tree.delete(item)
        
        if not agendamentos_periodo:
            # Se não houver agendamentos, mostrar mensagem
            self.services_tree.insert('', 'end', values=(
                "Nenhum agendamento concluído no período",
                "0",
                "R$ 0,00"
            ))
            return
        
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
        
        if not agendamentos_periodo:
            # Se não houver agendamentos, mostrar mensagem
            self.employees_tree.insert('', 'end', values=(
                "Nenhum agendamento concluído no período",
                "0",
                "R$ 0,00"
            ))
            return
        
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
    
    def export_relatorio(self):
        """Exporta relatório em arquivo TXT usando thread"""
        filename = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Arquivos de texto", "*.txt"), ("Todos os arquivos", "*.*")],
            title="Salvar Relatório"
        )
        
        if not filename:
            return
        
        try:
            data_inicial = datetime.strptime(self.data_inicial_var.get(), "%d/%m/%Y")
            data_final = datetime.strptime(self.data_final_var.get(), "%d/%m/%Y")
        except ValueError:
            messagebox.showerror("Erro", "Formato de data inválido. Use DD/MM/AAAA")
            return
        
        messagebox.showinfo("Exportando", "Exportando relatório em segundo plano...")
        
        def on_export_complete(success, result):
            if success:
                messagebox.showinfo("Sucesso", f"Relatório exportado com sucesso!\n\n{result}")
            else:
                messagebox.showerror("Erro", f"Erro ao exportar relatório:\n{result}")
        
        self.data_manager.export_relatorio_txt(
            self.clientes, self.funcionarios, self.servicos, self.agendamentos,
            data_inicial, data_final, filename, on_export_complete
        )
    
    def load_data_from_files(self):
        """Carrega dados dos arquivos usando threads"""
        from decimal import Decimal
        
        def on_clientes_loaded(clientes):
            self.clientes = clientes
            if not self.clientes:
                self.clientes = [
                    Cliente(1, "João Silva", "(11) 99999-9999", "joao@email.com", datetime.now(), "Cliente VIP", True),
                    Cliente(2, "Maria Santos", "(11) 88888-8888", "maria@email.com", datetime.now(), "", True),
                ]
            check_all_loaded()
        
        def on_funcionarios_loaded(funcionarios):
            self.funcionarios = funcionarios
            if not self.funcionarios:
                self.funcionarios = [
                    Funcionario(1, "Carlos Silva", "(11) 99999-9999", "carlos@barbearia.com", "Barbeiro", datetime.now(), 2500.00, True),
                    Funcionario(2, "Maria Santos", "(11) 88888-8888", "maria@barbearia.com", "Barbeira", datetime.now(), 2500.00, True),
                ]
            check_all_loaded()
        
        def on_servicos_loaded(servicos):
            self.servicos = servicos
            if not self.servicos:
                self.servicos = [
                    Servico(1, "Corte Masculino", "Corte de cabelo masculino tradicional", Decimal('25.00'), 30, True),
                    Servico(2, "Barba", "Aparar e modelar barba", Decimal('15.00'), 20, True),
                    Servico(3, "Corte + Barba", "Corte de cabelo + barba", Decimal('35.00'), 45, True),
                ]
            check_all_loaded()
        
        def on_agendamentos_loaded(agendamentos):
            self.agendamentos = agendamentos
            check_all_loaded()
        
        loaded_count = [0]
        def check_all_loaded():
            loaded_count[0] += 1
            if loaded_count[0] == 4:
                # Atualizar estatísticas após carregar todos os dados
                self.update_statistics()
        
        # Força recarregamento dos dados do arquivo
        self.data_manager.load_clientes(on_clientes_loaded)
        self.data_manager.load_funcionarios(on_funcionarios_loaded)
        self.data_manager.load_servicos(on_servicos_loaded)
        self.data_manager.load_agendamentos(on_agendamentos_loaded, force_reload=True)