import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from models import Servico
from decimal import Decimal

class ServicosWindow:
    """Janela de gerenciamento de serviços"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.window = None
        self.servicos: List[Servico] = []
        self.current_servico: Optional[Servico] = None
        self.create_window()
        self.load_sample_data()
        self.refresh_servicos_list()
    
    def create_window(self):
        """Cria a janela de gerenciamento de serviços"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Gerenciamento de Serviços")
        self.window.geometry("1000x700")
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
    
    def create_layout(self):
        """Cria o layout principal"""
        # Frame principal
        main_frame = ttk.Frame(self.window, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Título
        title_label = ttk.Label(
            main_frame, 
            text="Gerenciamento de Serviços", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame principal com duas colunas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Lista de serviços
        self.create_servicos_list(content_frame)
        
        # Coluna direita - Formulário
        self.create_servico_form(content_frame)
    
    def create_servicos_list(self, parent):
        """Cria a lista de serviços"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Lista de Serviços", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Novo", 
            command=self.new_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            action_frame, 
            text="Editar", 
            command=self.edit_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Excluir", 
            command=self.delete_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview para lista de serviços
        columns = ('Nome', 'Preço', 'Duração', 'Status')
        self.servicos_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.servicos_tree.heading('Nome', text='Nome')
        self.servicos_tree.heading('Preço', text='Preço')
        self.servicos_tree.heading('Duração', text='Duração (min)')
        self.servicos_tree.heading('Status', text='Status')
        
        self.servicos_tree.column('Nome', width=250)
        self.servicos_tree.column('Preço', width=100)
        self.servicos_tree.column('Duração', width=100)
        self.servicos_tree.column('Status', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.servicos_tree.yview)
        self.servicos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.servicos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind seleção
        self.servicos_tree.bind('<<TreeviewSelect>>', self.on_servico_select)
    
    def create_servico_form(self, parent):
        """Cria o formulário de serviço"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título do formulário
        ttk.Label(
            form_frame, 
            text="Dados do Serviço", 
            style='Title.TLabel'
        ).pack(pady=5)
        
        # Frame do formulário
        form_content = ttk.Frame(form_frame)
        form_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Campos do formulário
        self.create_form_fields(form_content)
        
        # Botões do formulário
        self.create_form_buttons(form_content)
    
    def create_form_fields(self, parent):
        """Cria os campos do formulário"""
        # Nome
        ttk.Label(parent, text="Nome *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.nome_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Preço
        ttk.Label(parent, text="Preço (R$) *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.preco_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.preco_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Duração
        ttk.Label(parent, text="Duração (min) *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.duracao_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.duracao_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Descrição
        ttk.Label(parent, text="Descrição:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.descricao_text = tk.Text(parent, width=30, height=4, font=('Arial', 10))
        self.descricao_text.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Status
        self.ativo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent, 
            text="Serviço Ativo", 
            variable=self.ativo_var
        ).grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_form_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Salvar", 
            command=self.save_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.cancel_edit,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame, 
            text="Limpar", 
            command=self.clear_form,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(10, 0))
    
    def load_sample_data(self):
        """Carrega dados de exemplo"""
        sample_servicos = [
            Servico(1, "Corte Masculino", "Corte de cabelo masculino tradicional", Decimal('25.00'), 30, True),
            Servico(2, "Barba", "Aparar e modelar barba", Decimal('15.00'), 20, True),
            Servico(3, "Corte + Barba", "Corte de cabelo + barba", Decimal('35.00'), 45, True),
            Servico(4, "Sobrancelha", "Aparar sobrancelhas", Decimal('10.00'), 15, True),
            Servico(5, "Corte Feminino", "Corte de cabelo feminino", Decimal('40.00'), 60, True),
            Servico(6, "Pintura", "Pintura de cabelo", Decimal('80.00'), 120, False),
        ]
        self.servicos = sample_servicos
    
    def refresh_servicos_list(self):
        """Atualiza a lista de serviços"""
        # Limpar lista
        for item in self.servicos_tree.get_children():
            self.servicos_tree.delete(item)
        
        # Adicionar serviços
        for servico in self.servicos:
            status = "Ativo" if servico.ativo else "Inativo"
            self.servicos_tree.insert('', 'end', values=(
                servico.nome,
                f"R$ {servico.preco:.2f}",
                servico.duracao_minutos,
                status
            ), tags=(servico.id,))
    
    def on_servico_select(self, event):
        """Callback quando um serviço é selecionado"""
        selection = self.servicos_tree.selection()
        if selection:
            item = self.servicos_tree.item(selection[0])
            servico_id = item['tags'][0] if item['tags'] else None
            
            if servico_id:
                servico = next((s for s in self.servicos if s.id == servico_id), None)
                if servico:
                    self.load_servico_to_form(servico)
    
    def load_servico_to_form(self, servico: Servico):
        """Carrega os dados do serviço no formulário"""
        self.current_servico = servico
        
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, servico.nome)
        
        self.preco_entry.delete(0, tk.END)
        self.preco_entry.insert(0, str(servico.preco))
        
        self.duracao_entry.delete(0, tk.END)
        self.duracao_entry.insert(0, str(servico.duracao_minutos))
        
        self.descricao_text.delete(1.0, tk.END)
        self.descricao_text.insert(1.0, servico.descricao)
        
        self.ativo_var.set(servico.ativo)
    
    def new_servico(self):
        """Cria um novo serviço"""
        self.clear_form()
        self.current_servico = None
        self.nome_entry.focus()
    
    def edit_servico(self):
        """Edita o serviço selecionado"""
        selection = self.servicos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço para editar.")
            return
        
        item = self.servicos_tree.item(selection[0])
        servico_id = item['tags'][0] if item['tags'] else None
        
        if servico_id:
            servico = next((s for s in self.servicos if s.id == servico_id), None)
            if servico:
                self.load_servico_to_form(servico)
    
    def delete_servico(self):
        """Exclui o serviço selecionado"""
        selection = self.servicos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço para excluir.")
            return
        
        item = self.servicos_tree.item(selection[0])
        servico_id = item['tags'][0] if item['tags'] else None
        
        if servico_id:
            servico = next((s for s in self.servicos if s.id == servico_id), None)
            if servico:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o serviço {servico.nome}?"):
                    servico.ativo = False
                    self.refresh_servicos_list()
                    self.clear_form()
                    messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
    
    def save_servico(self):
        """Salva o serviço"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        preco_str = self.preco_entry.get().strip()
        duracao_str = self.duracao_entry.get().strip()
        
        if not nome or not preco_str or not duracao_str:
            messagebox.showerror("Erro", "Nome, preço e duração são obrigatórios.")
            return
        
        try:
            preco = Decimal(preco_str)
            duracao = int(duracao_str)
            
            if preco < 0:
                messagebox.showerror("Erro", "O preço deve ser maior ou igual a zero.")
                return
            
            if duracao <= 0:
                messagebox.showerror("Erro", "A duração deve ser maior que zero.")
                return
                
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Preço e duração devem ser números válidos.")
            return
        
        # Criar ou atualizar serviço
        if self.current_servico:
            # Atualizar serviço existente
            self.current_servico.nome = nome
            self.current_servico.preco = preco
            self.current_servico.duracao_minutos = duracao
            self.current_servico.descricao = self.descricao_text.get(1.0, tk.END).strip()
            self.current_servico.ativo = self.ativo_var.get()
            messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
        else:
            # Criar novo serviço
            novo_id = max([s.id for s in self.servicos], default=0) + 1
            novo_servico = Servico(
                id=novo_id,
                nome=nome,
                preco=preco,
                duracao_minutos=duracao,
                descricao=self.descricao_text.get(1.0, tk.END).strip(),
                ativo=self.ativo_var.get()
            )
            self.servicos.append(novo_servico)
            messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
        
        self.refresh_servicos_list()
        self.clear_form()
    
    def cancel_edit(self):
        """Cancela a edição"""
        self.clear_form()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.current_servico = None
        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.duracao_entry.delete(0, tk.END)
        self.descricao_text.delete(1.0, tk.END)
        self.ativo_var.set(True)
        
        # Desmarcar seleção na lista
        for item in self.servicos_tree.selection():
            self.servicos_tree.selection_remove(item)
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()


class ServicosWidget:
    """Widget de gerenciamento de serviços para uso embutido"""
    
    def __init__(self, parent):
        self.parent = parent
        self.servicos: List[Servico] = []
        self.current_servico: Optional[Servico] = None
        self.create_widget()
        self.load_sample_data()
        self.refresh_servicos_list()
    
    def create_widget(self):
        """Cria o widget de serviços"""
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
    
    def create_layout(self):
        """Cria o layout principal"""
        # Frame principal centralizado
        content_frame = ttk.Frame(self.main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Container que ocupa toda a largura
        center_frame = ttk.Frame(content_frame)
        center_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Lista de serviços
        self.create_servicos_list(center_frame)
        
        # Coluna direita - Formulário
        self.create_servico_form(center_frame)
    
    def create_servicos_list(self, parent):
        """Cria a lista de serviços"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Lista de Serviços", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Novo", 
            command=self.new_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            action_frame, 
            text="Editar", 
            command=self.edit_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Excluir", 
            command=self.delete_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview para lista de serviços
        columns = ('Nome', 'Preço', 'Duração', 'Status')
        self.servicos_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar colunas
        self.servicos_tree.heading('Nome', text='Nome')
        self.servicos_tree.heading('Preço', text='Preço')
        self.servicos_tree.heading('Duração', text='Duração (min)')
        self.servicos_tree.heading('Status', text='Status')
        
        self.servicos_tree.column('Nome', width=200)
        self.servicos_tree.column('Preço', width=80)
        self.servicos_tree.column('Duração', width=80)
        self.servicos_tree.column('Status', width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.servicos_tree.yview)
        self.servicos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.servicos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind seleção
        self.servicos_tree.bind('<<TreeviewSelect>>', self.on_servico_select)
    
    def create_servico_form(self, parent):
        """Cria o formulário de serviço"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título do formulário
        ttk.Label(
            form_frame, 
            text="Dados do Serviço", 
            style='Title.TLabel'
        ).pack(pady=5)
        
        # Frame do formulário
        form_content = ttk.Frame(form_frame)
        form_content.pack(fill=tk.BOTH, expand=True, padx=5, pady=(0, 5))
        
        # Campos do formulário
        self.create_form_fields(form_content)
        
        # Botões do formulário
        self.create_form_buttons(form_content)
    
    def create_form_fields(self, parent):
        """Cria os campos do formulário"""
        # Nome
        ttk.Label(parent, text="Nome *:").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.nome_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.nome_entry.grid(row=0, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Preço
        ttk.Label(parent, text="Preço (R$) *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.preco_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.preco_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Duração
        ttk.Label(parent, text="Duração (min) *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.duracao_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.duracao_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Descrição
        ttk.Label(parent, text="Descrição:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.descricao_text = tk.Text(parent, width=25, height=3, font=('Arial', 10))
        self.descricao_text.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Status
        self.ativo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent, 
            text="Serviço Ativo", 
            variable=self.ativo_var
        ).grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_form_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=5, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Salvar", 
            command=self.save_servico,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(
            button_frame, 
            text="Cancelar", 
            command=self.cancel_edit,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Button(
            button_frame, 
            text="Limpar", 
            command=self.clear_form,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(10, 0))
    
    def load_sample_data(self):
        """Carrega dados de exemplo"""
        sample_servicos = [
            Servico(1, "Corte Masculino", "Corte de cabelo masculino tradicional", Decimal('25.00'), 30, True),
            Servico(2, "Barba", "Aparar e modelar barba", Decimal('15.00'), 20, True),
            Servico(3, "Corte + Barba", "Corte de cabelo + barba", Decimal('35.00'), 45, True),
            Servico(4, "Sobrancelha", "Aparar sobrancelhas", Decimal('10.00'), 15, True),
            Servico(5, "Corte Feminino", "Corte de cabelo feminino", Decimal('40.00'), 60, True),
            Servico(6, "Pintura", "Pintura de cabelo", Decimal('80.00'), 120, False),
        ]
        self.servicos = sample_servicos
    
    def refresh_servicos_list(self):
        """Atualiza a lista de serviços"""
        # Limpar lista
        for item in self.servicos_tree.get_children():
            self.servicos_tree.delete(item)
        
        # Adicionar serviços
        for servico in self.servicos:
            status = "Ativo" if servico.ativo else "Inativo"
            self.servicos_tree.insert('', 'end', values=(
                servico.nome,
                f"R$ {servico.preco:.2f}",
                servico.duracao_minutos,
                status
            ), tags=(servico.id,))
    
    def on_servico_select(self, event):
        """Callback quando um serviço é selecionado"""
        selection = self.servicos_tree.selection()
        if selection:
            item = self.servicos_tree.item(selection[0])
            servico_id = item['tags'][0] if item['tags'] else None
            
            if servico_id:
                servico = next((s for s in self.servicos if s.id == servico_id), None)
                if servico:
                    self.load_servico_to_form(servico)
    
    def load_servico_to_form(self, servico: Servico):
        """Carrega os dados do serviço no formulário"""
        self.current_servico = servico
        
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, servico.nome)
        
        self.preco_entry.delete(0, tk.END)
        self.preco_entry.insert(0, str(servico.preco))
        
        self.duracao_entry.delete(0, tk.END)
        self.duracao_entry.insert(0, str(servico.duracao_minutos))
        
        self.descricao_text.delete(1.0, tk.END)
        self.descricao_text.insert(1.0, servico.descricao)
        
        self.ativo_var.set(servico.ativo)
    
    def new_servico(self):
        """Cria um novo serviço"""
        self.clear_form()
        self.current_servico = None
        self.nome_entry.focus()
    
    def edit_servico(self):
        """Edita o serviço selecionado"""
        selection = self.servicos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço para editar.")
            return
        
        item = self.servicos_tree.item(selection[0])
        servico_id = item['tags'][0] if item['tags'] else None
        
        if servico_id:
            servico = next((s for s in self.servicos if s.id == servico_id), None)
            if servico:
                self.load_servico_to_form(servico)
    
    def delete_servico(self):
        """Exclui o serviço selecionado"""
        selection = self.servicos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço para excluir.")
            return
        
        item = self.servicos_tree.item(selection[0])
        servico_id = item['tags'][0] if item['tags'] else None
        
        if servico_id:
            servico = next((s for s in self.servicos if s.id == servico_id), None)
            if servico:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o serviço {servico.nome}?"):
                    servico.ativo = False
                    self.refresh_servicos_list()
                    self.clear_form()
                    messagebox.showinfo("Sucesso", "Serviço excluído com sucesso!")
    
    def save_servico(self):
        """Salva o serviço"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        preco_str = self.preco_entry.get().strip()
        duracao_str = self.duracao_entry.get().strip()
        
        if not nome or not preco_str or not duracao_str:
            messagebox.showerror("Erro", "Nome, preço e duração são obrigatórios.")
            return
        
        try:
            preco = Decimal(preco_str)
            duracao = int(duracao_str)
            
            if preco < 0:
                messagebox.showerror("Erro", "O preço deve ser maior ou igual a zero.")
                return
            
            if duracao <= 0:
                messagebox.showerror("Erro", "A duração deve ser maior que zero.")
                return
                
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Preço e duração devem ser números válidos.")
            return
        
        # Criar ou atualizar serviço
        if self.current_servico:
            # Atualizar serviço existente
            self.current_servico.nome = nome
            self.current_servico.preco = preco
            self.current_servico.duracao_minutos = duracao
            self.current_servico.descricao = self.descricao_text.get(1.0, tk.END).strip()
            self.current_servico.ativo = self.ativo_var.get()
            messagebox.showinfo("Sucesso", "Serviço atualizado com sucesso!")
        else:
            # Criar novo serviço
            novo_id = max([s.id for s in self.servicos], default=0) + 1
            novo_servico = Servico(
                id=novo_id,
                nome=nome,
                preco=preco,
                duracao_minutos=duracao,
                descricao=self.descricao_text.get(1.0, tk.END).strip(),
                ativo=self.ativo_var.get()
            )
            self.servicos.append(novo_servico)
            messagebox.showinfo("Sucesso", "Serviço cadastrado com sucesso!")
        
        self.refresh_servicos_list()
        self.clear_form()
    
    def cancel_edit(self):
        """Cancela a edição"""
        self.clear_form()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.current_servico = None
        self.nome_entry.delete(0, tk.END)
        self.preco_entry.delete(0, tk.END)
        self.duracao_entry.delete(0, tk.END)
        self.descricao_text.delete(1.0, tk.END)
        self.ativo_var.set(True)
        
        # Desmarcar seleção na lista
        for item in self.servicos_tree.selection():
            self.servicos_tree.selection_remove(item)