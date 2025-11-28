import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from ..models import Cliente
from ..repositories import get_api_client
from ..utils import bind_phone_mask, bind_email_validator, PhoneMask, EmailValidator
from .loading_widget import LoadingWidget

class ClientesWidget:
    """Widget de gerenciamento de clientes para uso embutido"""
    
    def __init__(self, parent, dashboard_callback=None):
        self.parent = parent
        self.clientes: List[Cliente] = []
        self.current_cliente: Optional[Cliente] = None
        self.api_client = get_api_client()
        self.dashboard_callback = dashboard_callback  # Callback para notificar dashboard
        self.loading_widget = None
        self.create_widget()
        self.load_data_from_file()
        # Não chamar refresh_clientes_list() aqui - será chamado quando os dados carregarem
    
    def load_data_from_file(self):
        """Carrega dados do banco de dados usando thread"""
        # Verificar se já tem cache e se a lista está vazia - se não tiver, mostrar loading
        if self.api_client._clientes is None and len(self.clientes) == 0:
            if self.loading_widget is None and hasattr(self, 'treeview_container'):
                # Esconder treeview temporariamente
                self.clientes_tree.pack_forget()
                # Mostrar loading no container
                self.loading_widget = LoadingWidget(self.treeview_container, "Carregando clientes")
                self.loading_widget.show()
        
        def on_data_loaded(clientes_loaded):
            # Agendar atualização da GUI na thread principal
            root = self.parent.winfo_toplevel()
            # Esconder loading e mostrar treeview
            if self.loading_widget:
                def hide_and_show():
                    self.loading_widget.hide()
                    self.clientes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                root.after(0, hide_and_show)
            # Atualizar apenas se houver dados válidos (não None)
            if clientes_loaded is not None:
                self.clientes = clientes_loaded
                root.after(0, self.refresh_clientes_list)
            # Se clientes_loaded for None, manter dados antigos (não atualizar)
        
        # NÃO limpar lista - manter dados antigos visíveis até novos chegarem
        # Isso evita que a interface fique "nugada" durante carregamento
        # Carrega dados em thread (se já houver cache, será retornado imediatamente)
        self.api_client.load_clientes(on_data_loaded)
    
    def create_widget(self):
        """Cria o widget de clientes"""
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
        
        # Coluna esquerda - Lista de clientes
        self.create_clientes_list(center_frame)
        
        # Coluna direita - Formulário
        self.create_client_form(center_frame)
    
    def create_clientes_list(self, parent):
        """Cria a lista de clientes"""
        list_frame = ttk.Frame(parent, style='Card.TFrame')
        list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 5))
        
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
        
        # Frame container para treeview/loading (alterna entre eles)
        self.treeview_container = ttk.Frame(list_frame)
        self.treeview_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Treeview para lista de clientes
        columns = ('Nome', 'Telefone', 'Email', 'Data Cadastro')
        self.clientes_tree = ttk.Treeview(self.treeview_container, columns=columns, show='headings', height=12)
        
        # Configurar colunas
        self.clientes_tree.heading('Nome', text='Nome')
        self.clientes_tree.heading('Telefone', text='Telefone')
        self.clientes_tree.heading('Email', text='Email')
        self.clientes_tree.heading('Data Cadastro', text='Data Cadastro')
        
        self.clientes_tree.column('Nome', width=150)
        self.clientes_tree.column('Telefone', width=100)
        self.clientes_tree.column('Email', width=150)
        self.clientes_tree.column('Data Cadastro', width=100)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(self.treeview_container, orient=tk.VERTICAL, command=self.clientes_tree.yview)
        self.clientes_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.clientes_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
        
        # Telefone
        ttk.Label(parent, text="Telefone *:").grid(row=1, column=0, sticky=tk.W, pady=5)
        telefone_frame = ttk.Frame(parent)
        telefone_frame.grid(row=1, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.telefone_entry = ttk.Entry(telefone_frame, width=20, font=('Arial', 10))
        self.telefone_entry.pack(side=tk.LEFT)
        bind_phone_mask(self.telefone_entry)
        ttk.Label(telefone_frame, text="(XX) XXXXX-XXXX", font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=(5, 0))
        
        # Email
        ttk.Label(parent, text="Email:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.email_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        bind_email_validator(self.email_entry)
        
        # Data de Cadastro
        ttk.Label(parent, text="Data Cadastro:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.data_cadastro_label = ttk.Label(parent, text="", style='Subtitle.TLabel')
        self.data_cadastro_label.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        
        # Observações
        ttk.Label(parent, text="Observações:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.observacoes_text = tk.Text(parent, width=25, height=3, font=('Arial', 10))
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
        button_frame.grid(row=6, column=0, columnspan=2, pady=5)
        
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
    
    
    def refresh_clientes_list(self):
        """Atualiza a lista de clientes"""
        # Verificar se o widget ainda existe
        try:
            if not hasattr(self, 'clientes_tree') or not self.clientes_tree.winfo_exists():
                return
        except:
            return
        
        # Limpar lista
        try:
            for item in self.clientes_tree.get_children():
                self.clientes_tree.delete(item)
        except:
            return
        
        # Adicionar clientes
        for cliente in self.clientes:
            if cliente.ativo:  # Mostrar apenas clientes ativos
                data_cadastro = cliente.data_cadastro.strftime("%d/%m/%Y") if cliente.data_cadastro else ""
                # Formatar telefone para exibição
                telefone_numeros = PhoneMask.get_numbers(cliente.telefone) if cliente.telefone else ""
                if telefone_numeros:
                    if len(telefone_numeros) == 10:
                        telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:6]}-{telefone_numeros[6:]}"
                    elif len(telefone_numeros) == 11:
                        telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
                    else:
                        telefone_formatado = cliente.telefone
                else:
                    telefone_formatado = cliente.telefone if cliente.telefone else ""
                
                self.clientes_tree.insert('', 'end', values=(
                    cliente.nome,
                    telefone_formatado,
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
        # Formatar telefone ao carregar
        telefone_numeros = PhoneMask.get_numbers(cliente.telefone) if cliente.telefone else ""
        if telefone_numeros:
            if len(telefone_numeros) == 10:
                telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:6]}-{telefone_numeros[6:]}"
            elif len(telefone_numeros) == 11:
                telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
            else:
                telefone_formatado = cliente.telefone
            self.telefone_entry.insert(0, telefone_formatado)
        else:
            self.telefone_entry.insert(0, cliente.telefone if cliente.telefone else "")
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, cliente.email if cliente.email else "")
        
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
                    # Salvar no banco de dados após exclusão
                    root = self.parent.winfo_toplevel()
                    def on_save_complete(success):
                        if success and self.dashboard_callback:
                            # Agendar notificação do dashboard na thread principal
                            root.after(0, self.dashboard_callback)
                    
                    self.api_client.save_clientes(self.clientes, on_save_complete)
                    self.refresh_clientes_list()
                    self.clear_form()
                    messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
    
    def save_cliente(self):
        """Salva o cliente usando thread"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        telefone = self.telefone_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório.")
            self.nome_entry.focus()
            return
        
        if not telefone:
            messagebox.showerror("Erro", "Telefone é obrigatório.")
            self.telefone_entry.focus()
            return
        
        # Validar formato do telefone
        if not PhoneMask.validate(telefone):
            messagebox.showerror("Erro", "Telefone inválido. Use o formato (XX) XXXXX-XXXX ou (XX) XXXX-XXXX")
            self.telefone_entry.focus()
            return
        
        # Validar formato do email (se preenchido)
        if email and not EmailValidator.validate(email):
            messagebox.showerror("Erro", "Email inválido. Verifique o formato do email.")
            self.email_entry.focus()
            return
        
        # Criar ou atualizar cliente
        if self.current_cliente:
            # Atualizar cliente existente
            self.current_cliente.nome = nome
            # Salvar telefone apenas com números
            self.current_cliente.telefone = PhoneMask.get_numbers(telefone)
            self.current_cliente.email = email
            self.current_cliente.observacoes = self.observacoes_text.get(1.0, tk.END).strip()
            self.current_cliente.ativo = self.ativo_var.get()
            messagebox.showinfo("Sucesso", "Cliente atualizado com sucesso!")
        else:
            # Criar novo cliente
            novo_id = max([c.id for c in self.clientes], default=0) + 1
            novo_cliente = Cliente(
                id=novo_id,
                nome=nome,
                telefone=PhoneMask.get_numbers(telefone),
                email=email,
                observacoes=self.observacoes_text.get(1.0, tk.END).strip(),
                ativo=self.ativo_var.get()
            )
            self.clientes.append(novo_cliente)
            messagebox.showinfo("Sucesso", "Cliente cadastrado com sucesso!")
        
        # Salvar no banco de dados usando thread
        root = self.parent.winfo_toplevel()
        def on_save_complete(success):
            if success and self.dashboard_callback:
                # Agendar notificação do dashboard na thread principal
                root.after(0, self.dashboard_callback)
        
        self.data_manager.save_clientes(self.clientes, on_save_complete)
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