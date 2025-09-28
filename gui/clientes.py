import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from models import Cliente
from datetime import datetime

class ClientesWindow:
    """Janela de gerenciamento de clientes"""
    
    def __init__(self, parent_window):
        self.parent = parent_window
        self.window = None
        self.clientes: List[Cliente] = []
        self.current_cliente: Optional[Cliente] = None
        self.create_window()
        self.load_sample_data()
        self.refresh_clientes_list()
    
    def create_window(self):
        """Cria a janela de gerenciamento de clientes"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Gerenciamento de Clientes")
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
            text="Gerenciamento de Clientes", 
            style='Title.TLabel'
        )
        title_label.pack(pady=(0, 20))
        
        # Frame principal com duas colunas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Coluna esquerda - Lista de clientes
        self.create_clientes_list(content_frame)
        
        # Coluna direita - Formulário
        self.create_client_form(content_frame)
    
    def create_clientes_list(self, parent):
        """Cria a lista de clientes"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Cabeçalho da lista
        header_frame = ttk.Frame(list_frame)
        header_frame.pack(fill=tk.X, padx=15, pady=15)
        
        ttk.Label(header_frame, text="Lista de Clientes", style='Title.TLabel').pack(side=tk.LEFT)
        
        # Botões de ação
        action_frame = ttk.Frame(header_frame)
        action_frame.pack(side=tk.RIGHT)
        
        ttk.Button(
            action_frame, 
            text="Novo", 
            command=self.new_cliente,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        ttk.Button(
            action_frame, 
            text="Editar", 
            command=self.edit_cliente,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(
            action_frame, 
            text="Excluir", 
            command=self.delete_cliente,
            style='Action.TButton'
        ).pack(side=tk.LEFT, padx=(5, 0))
        
        # Treeview para lista de clientes
        columns = ('Nome', 'Telefone', 'Email', 'Data Cadastro')
        self.clientes_tree = ttk.Treeview(list_frame, columns=columns, show='headings', height=15)
        
        # Configurar colunas
        self.clientes_tree.heading('Nome', text='Nome')
        self.clientes_tree.heading('Telefone', text='Telefone')
        self.clientes_tree.heading('Email', text='Email')
        self.clientes_tree.heading('Data Cadastro', text='Data Cadastro')
        
        self.clientes_tree.column('Nome', width=200)
        self.clientes_tree.column('Telefone', width=120)
        self.clientes_tree.column('Email', width=200)
        self.clientes_tree.column('Data Cadastro', width=120)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.clientes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y, pady=(0, 15))
        
        # Bind seleção
        self.clientes_tree.bind('<<TreeviewSelect>>', self.on_cliente_select)
    
    def create_client_form(self, parent):
        """Cria o formulário de cliente"""
        form_frame = ttk.Frame(parent, style='Card.TFrame')
        form_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # Título do formulário
        ttk.Label(
            form_frame, 
            text="Dados do Cliente", 
            style='Title.TLabel'
        ).pack(pady=15)
        
        # Frame do formulário
        form_content = ttk.Frame(form_frame)
        form_content.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 20))
        
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
        
        # Telefone
        ttk.Label(parent, text="Telefone *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.telefone_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.telefone_entry.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Email
        ttk.Label(parent, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(parent, width=30, font=('Arial', 10))
        self.email_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Data de Cadastro
        ttk.Label(parent, text="Data Cadastro:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.data_cadastro_label = ttk.Label(parent, text="", style='Subtitle.TLabel')
        self.data_cadastro_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Observações
        ttk.Label(parent, text="Observações:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.observacoes_text = tk.Text(parent, width=30, height=4, font=('Arial', 10))
        self.observacoes_text.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Status
        self.ativo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            parent, 
            text="Cliente Ativo", 
            variable=self.ativo_var
        ).grid(row=5, column=1, sticky=tk.W, padx=(10, 0), pady=5)
    
    def create_form_buttons(self, parent):
        """Cria os botões do formulário"""
        button_frame = ttk.Frame(parent)
        button_frame.grid(row=6, column=0, columnspan=2, pady=20)
        
        ttk.Button(
            button_frame, 
            text="Salvar", 
            command=self.save_cliente,
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
        sample_clientes = [
            Cliente(1, "João Silva", "(11) 99999-9999", "joao@email.com", datetime.now(), "Cliente VIP", True),
            Cliente(2, "Maria Santos", "(11) 88888-8888", "maria@email.com", datetime.now(), "", True),
            Cliente(3, "Pedro Oliveira", "(11) 77777-7777", "pedro@email.com", datetime.now(), "Prefere corte tradicional", True),
            Cliente(4, "Ana Costa", "(11) 66666-6666", "ana@email.com", datetime.now(), "", False),
        ]
        self.clientes = sample_clientes
    
    def refresh_clientes_list(self):
        """Atualiza a lista de clientes"""
        # Limpar lista
        for item in self.clientes_tree.get_children():
            self.clientes_tree.delete(item)
        
        # Adicionar clientes
        for cliente in self.clientes:
            if cliente.ativo:  # Mostrar apenas clientes ativos
                data_cadastro = cliente.data_cadastro.strftime("%d/%m/%Y") if cliente.data_cadastro else ""
                self.clientes_tree.insert('', 'end', values=(
                    cliente.nome,
                    cliente.telefone,
                    cliente.email,
                    data_cadastro
                ), tags=(cliente.id,))
    
    def on_cliente_select(self, event):
        """Callback quando um cliente é selecionado"""
        selection = self.clientes_tree.selection()
        if selection:
            item = self.clientes_tree.item(selection[0])
            cliente_id = item['tags'][0] if item['tags'] else None
            
            if cliente_id:
                cliente = next((c for c in self.clientes if c.id == cliente_id), None)
                if cliente:
                    self.load_cliente_to_form(cliente)
    
    def load_cliente_to_form(self, cliente: Cliente):
        """Carrega os dados do cliente no formulário"""
        self.current_cliente = cliente
        
        self.nome_entry.delete(0, tk.END)
        self.nome_entry.insert(0, cliente.nome)
        
        self.telefone_entry.delete(0, tk.END)
        self.telefone_entry.insert(0, cliente.telefone)
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, cliente.email)
        
        data_cadastro = cliente.data_cadastro.strftime("%d/%m/%Y %H:%M") if cliente.data_cadastro else ""
        self.data_cadastro_label.config(text=data_cadastro)
        
        self.observacoes_text.delete(1.0, tk.END)
        self.observacoes_text.insert(1.0, cliente.observacoes)
        
        self.ativo_var.set(cliente.ativo)
    
    def new_cliente(self):
        """Cria um novo cliente"""
        self.clear_form()
        self.current_cliente = None
        self.nome_entry.focus()
    
    def edit_cliente(self):
        """Edita o cliente selecionado"""
        selection = self.clientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para editar.")
            return
        
        item = self.clientes_tree.item(selection[0])
        cliente_id = item['tags'][0] if item['tags'] else None
        
        if cliente_id:
            cliente = next((c for c in self.clientes if c.id == cliente_id), None)
            if cliente:
                self.load_cliente_to_form(cliente)
    
    def delete_cliente(self):
        """Exclui o cliente selecionado"""
        selection = self.clientes_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um cliente para excluir.")
            return
        
        item = self.clientes_tree.item(selection[0])
        cliente_id = item['tags'][0] if item['tags'] else None
        
        if cliente_id:
            cliente = next((c for c in self.clientes if c.id == cliente_id), None)
            if cliente:
                if messagebox.askyesno("Confirmar", f"Deseja realmente excluir o cliente {cliente.nome}?"):
                    cliente.ativo = False
                    self.refresh_clientes_list()
                    self.clear_form()
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    
    def save_cliente(self):
        """Salva o cliente"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        
        if not nome or not telefone:
            messagebox.showerror("Erro", "Nome e telefone são obrigatórios.")
            return
        
        # Criar ou atualizar cliente
        if self.current_cliente:
            # Atualizar cliente existente
            self.current_cliente.nome = nome
            self.current_cliente.telefone = telefone
            self.current_cliente.email = self.email_entry.get().strip()
            self.current_cliente.observacoes = self.observacoes_text.get(1.0, tk.END).strip()
            self.current_cliente.ativo = self.ativo_var.get()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        else:
            # Criar novo cliente
            novo_id = max([c.id for c in self.clientes], default=0) + 1
            novo_cliente = Cliente(
                id=novo_id,
                nome=nome,
                telefone=telefone,
                email=self.email_entry.get().strip(),
                observacoes=self.observacoes_text.get(1.0, tk.END).strip(),
                ativo=self.ativo_var.get()
            )
            self.clientes.append(novo_cliente)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        
        self.refresh_clientes_list()
        self.clear_form()
    
    def cancel_edit(self):
        """Cancela a edição"""
        self.clear_form()
    
    def clear_form(self):
        """Limpa o formulário"""
        self.current_cliente = None
        self.nome_entry.delete(0, tk.END)
        self.telefone_entry.delete(0, tk.END)
        self.email_entry.delete(0, tk.END)
        self.data_cadastro_label.config(text="")
        self.observacoes_text.delete(1.0, tk.END)
        self.ativo_var.set(True)
        
        # Desmarcar seleção na lista
        for item in self.clientes_tree.selection():
            self.clientes_tree.selection_remove(item)
    
    def run(self):
        """Executa a janela"""
        self.window.mainloop()
