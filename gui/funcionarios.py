import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from models import Funcionario
from datetime import datetime

class FuncionariosWindow:
    """Janela de gerenciamento de funcionários"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.window = None
        self.funcionarios: List[Funcionario] = []
        self.current_funcionario: Optional[Funcionario] = None
        self.create_window()
        self.load_sample_data()
        self.refresh_funcionarios_list()
    
    def create_window(self):
        """Cria a janela de gerenciamento de funcionários"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Gerenciamento de Funcionários")
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
            text="Gerenciamento de Funcionários", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame principal com duas colunas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Lista de funcionários
        self.create_funcionarios_list(content_frame)
        
        # Coluna direita - Formulário
        self.create_funcionario_form(content_frame)
    
    def create_funcionarios_list(self, parent):
        """Cria a lista de funcionários"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Lista de Funcionários", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Novo", 
            command=self.new_funcionario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            action_frame, 
            text="Editar", 
            command=self.edit_funcionario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Excluir", 
            command=self.delete_funcionario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview para lista de funcionários
        columns = ('Nome', 'Cargo', 'Telefone', 'Salário', 'Status')
        self.funcionarios_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.funcionarios_tree.heading('Nome', text='Nome')
        self.funcionarios_tree.heading('Cargo', text='Cargo')
        self.funcionarios_tree.heading('Telefone', text='Telefone')
        self.funcionarios_tree.heading('Salário', text='Salário')
        self.funcionarios_tree.heading('Status', text='Status')
        
        self.funcionarios_tree.column('Nome', width=200)
        self.funcionarios_tree.column('Cargo', width=150)
        self.funcionarios_tree.column('Telefone', width=120)
        self.funcionarios_tree.column('Salário', width=100)
        self.funcionarios_tree.column('Status', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.funcionarios_tree.yview)
        self.funcionarios_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.funcionarios_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind seleção
        self.funcionarios_tree.bind('<<TreeviewSelect>>', self.on_funcionario_select)
    
    def create_funcionario_form(self, parent):
        """Cria o formulário de funcionário"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título do formulário
        ttk.Label(
            form_frame, 
            text="Dados do Funcionário", 
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
        
        # Cargo
        ttk.Label(parent, text="Cargo *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cargo_combo = ttk.Combobox(parent, width=27, font=('Arial', 10), state='readonly')
        self.cargo_combo['values'] = ('Barbeiro', 'Barbeira', 'Recepcionista', 'Gerente', 'Auxiliar')
        self.cargo_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Telefone
        ttk.Label(parent, text="Telefone *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.telefone_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.telefone_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Email
        ttk.Label(parent, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.email_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Salário
        ttk.Label(parent, text="Salário (R$) *:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.salario_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.salario_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Data de Admissão
        ttk.Label(parent, text="Data Admissão:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.data_admissao_label = ttk.Label(parent, text="", style='Subtitle.TLabel')
        self.data_admissao_label.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Status
        self.ativo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent, 
            text="Funcionário Ativo", 
            variable=self.ativo_var
        ).grid(row=6, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_form_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=7, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Salvar", 
            command=self.save_funcionario,
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
        sample_funcionarios = [
            Funcionario(1, "Carlos Silva", "(11) 99999-9999", "carlos@barbearia.com", "Barbeiro", datetime.now(), 2500.00, True),
            Funcionario(2, "Maria Santos", "(11) 88888-8888", "maria@barbearia.com", "Barbeira", datetime.now(), 2500.00, True),
            Funcionario(3, "Ana Costa", "(11) 77777-7777", "ana@barbearia.com", "Recepcionista", datetime.now(), 1800.00, True),
            Funcionario(4, "João Oliveira", "(11) 66666-6666", "joao@barbearia.com", "Gerente", datetime.now(), 3500.00, True),
            Funcionario(5, "Pedro Lima", "(11) 55555-5555", "pedro@barbearia.com", "Barbeiro", datetime.now(), 2500.00, False),
        ]
        self.funcionarios = sample_funcionarios
    
    def refresh_funcionarios_list(self):
        """Atualiza a lista de funcionários"""
        # Limpar lista
        for item in self.funcionarios_tree.get_children():
            self.funcionarios_tree.delete(item)
        
        # Adicionar funcionários
        for funcionario in self.funcionarios:
            status = "Ativo" if funcionario.ativo else "Inativo"
            self.funcionarios_tree.insert('', 'end', values=(
                funcionario.nome,
                funcionario.cargo,
                funcionario.telefone,
                f"R$ {funcionario.salario:.2f}",
                status
            ), tags=(funcionario.id,))
    
    def on_funcionario_select(self, event):
        """Callback quando um funcionário é selecionado"""
        selection = self.funcionarios_tree.selection()
        if selection:
            item = self.funcionarios_tree.item(selection[0])
            funcionario_id = item['tags'][0] if item['tags'] else None
            
            if funcionario_id:
                funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
                if funcionario:
                    self.load_funcionario_to_form(funcionario)
    
    def load_funcionario_to_form(self, funcionario: Funcionario):
        """Carrega os dados do funcionário no formulário"""
        self.current_funcionario = funcionario
        
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, funcionario.nome)
        
        self.cargo_combo.set(funcionario.cargo)
        
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, funcionario.telefone)
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, funcionario.email)
        
        self.salario_entry.delete(0, tk.END)
        self.salario_entry.insert(0, str(funcionario.salario))
        
        data_admissao = funcionario.data_admissao.strftime("%d/%m/%Y") if funcionario.data_admissao else ""
        self.data_admissao_label.config(text=data_admissao)
        
        self.ativo_var.set(funcionario.ativo)
    
    def new_funcionario(self):
        """Cria um novo funcionário"""
        self.clear_form()
        self.current_funcionario = None
        self.nome_entry.focus()
    
    def edit_funcionario(self):
        """Edita o funcionário selecionado"""
        selection = self.funcionarios_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um funcionário para editar.")
            return
        
        item = self.funcionarios_tree.item(selection[0])
        funcionario_id = item['tags'][0] if item['tags'] else None
        
        if funcionario_id:
            funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
            if funcionario:
                self.load_funcionario_to_form(funcionario)
    
    def delete_funcionario(self):
        """Exclui o funcionário selecionado"""
        selection = self.funcionarios_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir.")
            return
        
        item = self.funcionarios_tree.item(selection[0])
        funcionario_id = item['tags'][0] if item['tags'] else None
        
        if funcionario_id:
            funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
            if funcionario:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o funcionário {funcionario.nome}?"):
                    funcionario.ativo = False
                    self.refresh_funcionarios_list()
                    self.clear_form()
                    messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
    
    def save_funcionario(self):
        """Salva o funcionário"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        cargo = self.cargo_combo.get().strip()
        telefone = self.telefone_entry.get().strip()
        salario_str = self.salario_entry.get().strip()
        
        if not nome or not cargo or not telefone or not salario_str:
            messagebox.showerror("Erro", "Nome, cargo, telefone e salário são obrigatórios.")
            return
        
        try:
            salario = float(salario_str)
            if salario < 0:
                messagebox.showerror("Erro", "O salário deve ser maior ou igual a zero.")
                return
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Salário deve ser um número válido.")
            return
        
        # Criar ou atualizar funcionário
        if self.current_funcionario:
            # Atualizar funcionário existente
            self.current_funcionario.nome = nome
            self.current_funcionario.cargo = cargo
            self.current_funcionario.telefone = telefone
            self.current_funcionario.email = self.email_entry.get().strip()
            self.current_funcionario.salario = salario
            self.current_funcionario.ativo = self.ativo_var.get()
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        else:
            # Criar novo funcionário
            novo_id = max([f.id for f in self.funcionarios], default=0) + 1
            novo_funcionario = Funcionario(
                id=novo_id,
                nome=nome,
                cargo=cargo,
                telefone=telefone,
                email=self.email_entry.get().strip(),
                salario=salario,
                ativo=self.ativo_var.get()
            )
            self.funcionarios.append(novo_funcionario)
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        
        self.refresh_funcionarios_list()
        self.clear_form()
    
    def cancel_edit(self):
        """Cancela a edição"""
        self.clear_form()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.current_funcionario = None
        self.nome_entry.delete(0, tk.END)
        self.cargo_combo.set('')
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.salario_entry.delete(0, tk.END)
        self.data_admissao_label.config(text="")
        self.ativo_var.set(True)
        
        # Desmarcar seleção na lista
        for item in self.funcionarios_tree.selection():
            self.funcionarios_tree.selection_remove(item)
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()


class FuncionariosWidget:
    """Widget de gerenciamento de funcionários para uso embutido"""
    
    def __init__(self, parent):
        self.parent = parent
        self.funcionarios: List[Funcionario] = []
        self.current_funcionario: Optional[Funcionario] = None
        self.create_widget()
        self.load_sample_data()
        self.refresh_funcionarios_list()
    
    def create_widget(self):
        """Cria o widget de funcionários"""
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
        
        # Coluna esquerda - Lista de funcionários
        self.create_funcionarios_list(center_frame)
        
        # Coluna direita - Formulário
        self.create_funcionario_form(center_frame)
    
    def create_funcionarios_list(self, parent):
        """Cria a lista de funcionários"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Lista de Funcionários", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Novo", 
            command=self.new_funcionario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            action_frame, 
            text="Editar", 
            command=self.edit_funcionario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Excluir", 
            command=self.delete_funcionario,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview para lista de funcionários
        columns = ('Nome', 'Cargo', 'Telefone', 'Salário', 'Status')
        self.funcionarios_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=12)
        
        # Configurar colunas
        self.funcionarios_tree.heading('Nome', text='Nome')
        self.funcionarios_tree.heading('Cargo', text='Cargo')
        self.funcionarios_tree.heading('Telefone', text='Telefone')
        self.funcionarios_tree.heading('Salário', text='Salário')
        self.funcionarios_tree.heading('Status', text='Status')
        
        self.funcionarios_tree.column('Nome', width=150)
        self.funcionarios_tree.column('Cargo', width=120)
        self.funcionarios_tree.column('Telefone', width=100)
        self.funcionarios_tree.column('Salário', width=80)
        self.funcionarios_tree.column('Status', width=60)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.funcionarios_tree.yview)
        self.funcionarios_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.funcionarios_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind seleção
        self.funcionarios_tree.bind('<<TreeviewSelect>>', self.on_funcionario_select)
    
    def create_funcionario_form(self, parent):
        """Cria o formulário de funcionário"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título do formulário
        ttk.Label(
            form_frame, 
            text="Dados do Funcionário", 
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
        
        # Cargo
        ttk.Label(parent, text="Cargo *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.cargo_combo = ttk.Combobox(parent, width=22, font=('Arial', 10), state='readonly')
        self.cargo_combo['values'] = ('Barbeiro', 'Barbeira', 'Recepcionista', 'Gerente', 'Auxiliar')
        self.cargo_combo.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Telefone
        ttk.Label(parent, text="Telefone *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.telefone_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.telefone_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Email
        ttk.Label(parent, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.email_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Salário
        ttk.Label(parent, text="Salário (R$) *:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.salario_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.salario_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Data de Admissão
        ttk.Label(parent, text="Data Admissão:").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.data_admissao_label = ttk.Label(parent, text="", style='Subtitle.TLabel')
        self.data_admissao_label.grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Status
        self.ativo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent, 
            text="Funcionário Ativo", 
            variable=self.ativo_var
        ).grid(row=6, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_form_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=7, column=0, columnspan=2, pady=5)
        
        ttk.Button(
            button_frame, 
            text="Salvar", 
            command=self.save_funcionario,
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
        sample_funcionarios = [
            Funcionario(1, "Carlos Silva", "(11) 99999-9999", "carlos@barbearia.com", "Barbeiro", datetime.now(), 2500.00, True),
            Funcionario(2, "Maria Santos", "(11) 88888-8888", "maria@barbearia.com", "Barbeira", datetime.now(), 2500.00, True),
            Funcionario(3, "Ana Costa", "(11) 77777-7777", "ana@barbearia.com", "Recepcionista", datetime.now(), 1800.00, True),
            Funcionario(4, "João Oliveira", "(11) 66666-6666", "joao@barbearia.com", "Gerente", datetime.now(), 3500.00, True),
            Funcionario(5, "Pedro Lima", "(11) 55555-5555", "pedro@barbearia.com", "Barbeiro", datetime.now(), 2500.00, False),
        ]
        self.funcionarios = sample_funcionarios
    
    def refresh_funcionarios_list(self):
        """Atualiza a lista de funcionários"""
        # Limpar lista
        for item in self.funcionarios_tree.get_children():
            self.funcionarios_tree.delete(item)
        
        # Adicionar funcionários
        for funcionario in self.funcionarios:
            status = "Ativo" if funcionario.ativo else "Inativo"
            self.funcionarios_tree.insert('', 'end', values=(
                funcionario.nome,
                funcionario.cargo,
                funcionario.telefone,
                f"R$ {funcionario.salario:.2f}",
                status
            ), tags=(funcionario.id,))
    
    def on_funcionario_select(self, event):
        """Callback quando um funcionário é selecionado"""
        selection = self.funcionarios_tree.selection()
        if selection:
            item = self.funcionarios_tree.item(selection[0])
            funcionario_id = item['tags'][0] if item['tags'] else None
            
            if funcionario_id:
                funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
                if funcionario:
                    self.load_funcionario_to_form(funcionario)
    
    def load_funcionario_to_form(self, funcionario: Funcionario):
        """Carrega os dados do funcionário no formulário"""
        self.current_funcionario = funcionario
        
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, funcionario.nome)
        
        self.cargo_combo.set(funcionario.cargo)
        
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, funcionario.telefone)
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, funcionario.email)
        
        self.salario_entry.delete(0, tk.END)
        self.salario_entry.insert(0, str(funcionario.salario))
        
        data_admissao = funcionario.data_admissao.strftime("%d/%m/%Y") if funcionario.data_admissao else ""
        self.data_admissao_label.config(text=data_admissao)
        
        self.ativo_var.set(funcionario.ativo)
    
    def new_funcionario(self):
        """Cria um novo funcionário"""
        self.clear_form()
        self.current_funcionario = None
        self.nome_entry.focus()
    
    def edit_funcionario(self):
        """Edita o funcionário selecionado"""
        selection = self.funcionarios_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um funcionário para editar.")
            return
        
        item = self.funcionarios_tree.item(selection[0])
        funcionario_id = item['tags'][0] if item['tags'] else None
        
        if funcionario_id:
            funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
            if funcionario:
                self.load_funcionario_to_form(funcionario)
    
    def delete_funcionario(self):
        """Exclui o funcionário selecionado"""
        selection = self.funcionarios_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir.")
            return
        
        item = self.funcionarios_tree.item(selection[0])
        funcionario_id = item['tags'][0] if item['tags'] else None
        
        if funcionario_id:
            funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
            if funcionario:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o funcionário {funcionario.nome}?"):
                    funcionario.ativo = False
                    self.refresh_funcionarios_list()
                    self.clear_form()
                    messagebox.showinfo("Sucesso", "Funcionário excluído com sucesso!")
    
    def save_funcionario(self):
        """Salva o funcionário"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        cargo = self.cargo_combo.get().strip()
        telefone = self.telefone_entry.get().strip()
        salario_str = self.salario_entry.get().strip()
        
        if not nome or not cargo or not telefone or not salario_str:
            messagebox.showerror("Erro", "Nome, cargo, telefone e salário são obrigatórios.")
            return
        
        try:
            salario = float(salario_str)
            if salario < 0:
                messagebox.showerror("Erro", "O salário deve ser maior ou igual a zero.")
                return
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Salário deve ser um número válido.")
            return
        
        # Criar ou atualizar funcionário
        if self.current_funcionario:
            # Atualizar funcionário existente
            self.current_funcionario.nome = nome
            self.current_funcionario.cargo = cargo
            self.current_funcionario.telefone = telefone
            self.current_funcionario.email = self.email_entry.get().strip()
            self.current_funcionario.salario = salario
            self.current_funcionario.ativo = self.ativo_var.get()
            messagebox.showinfo("Sucesso", "Funcionário atualizado com sucesso!")
        else:
            # Criar novo funcionário
            novo_id = max([f.id for f in self.funcionarios], default=0) + 1
            novo_funcionario = Funcionario(
                id=novo_id,
                nome=nome,
                cargo=cargo,
                telefone=telefone,
                email=self.email_entry.get().strip(),
                salario=salario,
                ativo=self.ativo_var.get()
            )
            self.funcionarios.append(novo_funcionario)
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        
        self.refresh_funcionarios_list()
        self.clear_form()
    
    def cancel_edit(self):
        """Cancela a edição"""
        self.clear_form()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.current_funcionario = None
        self.nome_entry.delete(0, tk.END)
        self.cargo_combo.set('')
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.salario_entry.delete(0, tk.END)
        self.data_admissao_label.config(text="")
        self.ativo_var.set(True)
        
        # Desmarcar seleção na lista
        for item in self.funcionarios_tree.selection():
            self.funcionarios_tree.selection_remove(item)