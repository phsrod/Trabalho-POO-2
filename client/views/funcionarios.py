import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from datetime import datetime
from ..models import Funcionario
from ..repositories import get_api_client
from ..utils import bind_phone_mask, bind_email_validator, bind_money_mask, PhoneMask, EmailValidator, MoneyMask
from .loading_widget import LoadingWidget

class FuncionariosWidget:
    """Widget de gerenciamento de funcionários para uso embutido"""
    
    def __init__(self, parent, dashboard_callback=None):
        self.parent = parent
        self.funcionarios: List[Funcionario] = []
        self.current_funcionario: Optional[Funcionario] = None
        self.api_client = get_api_client()
        self.dashboard_callback = dashboard_callback  # Callback para notificar dashboard
        self.loading_widget = None
        self.create_widget()
        self.load_data_from_file()
        # Não chamar refresh_funcionarios_list() aqui - será chamado quando os dados carregarem
    
    def load_data_from_file(self):
        """Carrega dados do banco de dados usando thread"""
        # Verificar se já tem cache e se a lista está vazia - se não tiver, mostrar loading
        if self.api_client._funcionarios is None and len(self.funcionarios) == 0:
            if self.loading_widget is None and hasattr(self, 'treeview_container'):
                # Esconder treeview temporariamente
                self.funcionarios_tree.pack_forget()
                # Mostrar loading no container
                self.loading_widget = LoadingWidget(self.treeview_container, "Carregando funcionários")
                self.loading_widget.show()
        
        def on_data_loaded(funcionarios_loaded):
            # Agendar atualização da GUI na thread principal
            root = self.parent.winfo_toplevel()
            # Esconder loading e mostrar treeview
            if self.loading_widget:
                def hide_and_show():
                    self.loading_widget.hide()
                    self.funcionarios_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                root.after(0, hide_and_show)
            # Atualizar apenas se houver dados válidos (não None)
            if funcionarios_loaded is not None:
                self.funcionarios = funcionarios_loaded
                root.after(0, self.refresh_funcionarios_list)
            # Se funcionarios_loaded for None, manter dados antigos (não atualizar)
        
        # NÃO limpar lista - manter dados antigos visíveis até novos chegarem
        # Isso evita que a interface fique "nugada" durante carregamento
        # Carrega dados em thread (se já houver cache, será retornado imediatamente)
        self.api_client.load_funcionarios(on_data_loaded)
    
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
        
        # Campo de busca
        search_frame = ttk.Frame(list_frame)
        search_frame.pack(fill=tk.X, padx=15, pady=(0, 10))
        
        ttk.Label(search_frame, text="Buscar:", style='Subtitle.TLabel').pack(side=tk.LEFT, padx=(0, 5))
        self.search_entry = ttk.Entry(search_frame, font=('Arial', 10))
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.search_entry.bind('<KeyRelease>', lambda e: self.on_search_change())
        
        ttk.Button(
            search_frame,
            text="Limpar",
            command=self.clear_search,
            style='Action.TButton'
        ).pack(side=tk.LEFT)
        
        # Frame container para treeview/loading (alterna entre eles)
        self.treeview_container = ttk.Frame(list_frame)
        self.treeview_container.pack(fill=tk.BOTH, expand=True, padx=15, pady=(0, 15))
        
        # Treeview para lista de funcionários
        columns = ('Nome', 'Cargo', 'Telefone', 'Salário', 'Status')
        self.funcionarios_tree = ttk.Treeview(self.treeview_container, columns=columns, show='headings', height=12)
        
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
        scrollbar = ttk.Scrollbar(self.treeview_container, orient=tk.VERTICAL, command=self.funcionarios_tree.yview)
        self.funcionarios_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.funcionarios_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
        telefone_frame = ttk.Frame(parent)
        telefone_frame.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        self.telefone_entry = ttk.Entry(telefone_frame, width=20, font=('Arial', 10))
        self.telefone_entry.pack(side=tk.LEFT)
        bind_phone_mask(self.telefone_entry)
        ttk.Label(telefone_frame, text="(XX) XXXXX-XXXX", font=('Arial', 8), foreground='gray').pack(side=tk.LEFT, padx=(5, 0))
        
        # Email
        ttk.Label(parent, text="Email:").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.email_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.email_entry.grid(row=3, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        bind_email_validator(self.email_entry)
        
        # Salário
        ttk.Label(parent, text="Salário (R$) *:").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.salario_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.salario_entry.grid(row=4, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        bind_money_mask(self.salario_entry)
        
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

    
    def refresh_funcionarios_list(self):
        """Atualiza a lista de funcionários"""
        # Verificar se o widget ainda existe
        try:
            if not hasattr(self, 'funcionarios_tree') or not self.funcionarios_tree.winfo_exists():
                return
        except:
            return
        
        # Limpar lista
        try:
            for item in self.funcionarios_tree.get_children():
                self.funcionarios_tree.delete(item)
        except:
            return
        
        # Obter termo de busca
        search_term = ""
        if hasattr(self, 'search_entry'):
            try:
                search_term = self.search_entry.get().strip().lower()
            except:
                pass
        
        # Adicionar funcionários
        for funcionario in self.funcionarios:
            # Filtrar por busca se houver termo
            if search_term and search_term not in funcionario.nome.lower():
                continue
            
            status = "Ativo" if funcionario.ativo else "Inativo"
            # Formatar telefone para exibição
            telefone_numeros = PhoneMask.get_numbers(funcionario.telefone) if funcionario.telefone else ""
            if telefone_numeros:
                if len(telefone_numeros) == 10:
                    telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:6]}-{telefone_numeros[6:]}"
                elif len(telefone_numeros) == 11:
                    telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
                else:
                    telefone_formatado = funcionario.telefone
            else:
                telefone_formatado = funcionario.telefone if funcionario.telefone else ""
            
            # Formatar salário para exibição
            salario_formatado = MoneyMask.format_value(funcionario.salario)
            
            # Aplicar cor diferente para inativos
            tags = (funcionario.id,)
            if not funcionario.ativo:
                tags = (funcionario.id, 'inativo',)
            
            self.funcionarios_tree.insert('', 'end', values=(
                funcionario.nome,
                funcionario.cargo,
                telefone_formatado,
                salario_formatado,
                status
            ), tags=tags)
        
        # Configurar cor para inativos
        try:
            self.funcionarios_tree.tag_configure('inativo', foreground='gray')
        except:
            pass
    
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
        # Formatar telefone ao carregar
        telefone_numeros = PhoneMask.get_numbers(funcionario.telefone) if funcionario.telefone else ""
        if telefone_numeros:
            if len(telefone_numeros) == 10:
                telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:6]}-{telefone_numeros[6:]}"
            elif len(telefone_numeros) == 11:
                telefone_formatado = f"({telefone_numeros[:2]}) {telefone_numeros[2:7]}-{telefone_numeros[7:]}"
            else:
                telefone_formatado = funcionario.telefone
            self.telefone_entry.insert(0, telefone_formatado)
        else:
            self.telefone_entry.insert(0, funcionario.telefone if funcionario.telefone else "")
        
        self.email_entry.delete(0, tk.END)
        self.email_entry.insert(0, funcionario.email if funcionario.email else "")
        
        self.salario_entry.delete(0, tk.END)
        # Formatar salário como moeda
        self.salario_entry.insert(0, MoneyMask.format_value(funcionario.salario))
        
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
        """Remove o funcionário selecionado do banco de dados"""
        selection = self.funcionarios_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um funcionário para excluir.")
            return
        
        item = self.funcionarios_tree.item(selection[0])
        funcionario_id = item['tags'][0] if item['tags'] else None
        
        if funcionario_id:
            funcionario = next((f for f in self.funcionarios if f.id == funcionario_id), None)
            if funcionario:
                if messagebox.askyesno("Confirmar", f"Deseja realmente EXCLUIR permanentemente o funcionário {funcionario.nome}?\n\nEsta ação não pode ser desfeita!"):
                    root = self.parent.winfo_toplevel()
                    def on_delete_complete(success):
                        if success:
                            # Remover da lista local
                            self.funcionarios = [f for f in self.funcionarios if f.id != funcionario_id]
                            root.after(0, self.refresh_funcionarios_list)
                            root.after(0, self.clear_form)
                            root.after(0, lambda: messagebox.showinfo("Sucesso", "Funcionário excluído permanentemente do banco de dados!"))
                            if self.dashboard_callback:
                                root.after(0, self.dashboard_callback)
                        else:
                            root.after(0, lambda: messagebox.showerror("Erro", "Erro ao excluir funcionário. Tente novamente."))
                    
                    self.api_client.delete_funcionario(funcionario_id, on_delete_complete)
    
    def on_search_change(self):
        """Callback quando o campo de busca muda"""
        self.refresh_funcionarios_list()
    
    def clear_search(self):
        """Limpa o campo de busca"""
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
            self.refresh_funcionarios_list()
    
    def save_funcionario(self):
        """Salva o funcionário usando thread"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        cargo = self.cargo_combo.get().strip()
        telefone = self.telefone_entry.get().strip()
        salario_str = self.salario_entry.get().strip()
        email = self.email_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório.")
            self.nome_entry.focus()
            return
        
        if not cargo:
            messagebox.showerror("Erro", "Cargo é obrigatório.")
            self.cargo_combo.focus()
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
        
        if not salario_str:
            messagebox.showerror("Erro", "Salário é obrigatório.")
            self.salario_entry.focus()
            return
        
        # Formatar campo monetário se ainda não estiver formatado
        if not salario_str.startswith('R$'):
            # Formata antes de extrair o valor
            formatted = MoneyMask.format_value_string(salario_str)
            if formatted:
                self.salario_entry.delete(0, tk.END)
                self.salario_entry.insert(0, formatted)
                salario_str = formatted
        
        try:
            # Extrair valor numérico do campo monetário
            salario = MoneyMask.get_value(salario_str)
            if salario < 0:
                messagebox.showerror("Erro", "O salário deve ser maior ou igual a zero.")
                self.salario_entry.focus()
                return
        except (ValueError, TypeError):
            messagebox.showerror("Erro", "Salário deve ser um número válido.")
            self.salario_entry.focus()
            return
        
        # Criar ou atualizar funcionário
        if self.current_funcionario:
            # Atualizar funcionário existente
            self.current_funcionario.nome = nome
            self.current_funcionario.cargo = cargo
            # Salvar telefone apenas com números
            self.current_funcionario.telefone = PhoneMask.get_numbers(telefone)
            self.current_funcionario.email = email
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
                telefone=PhoneMask.get_numbers(telefone),
                email=email,
                salario=salario,
                ativo=self.ativo_var.get()
            )
            self.funcionarios.append(novo_funcionario)
            messagebox.showinfo("Sucesso", "Funcionário cadastrado com sucesso!")
        
        # Salvar no banco de dados usando thread
        root = self.parent.winfo_toplevel()
        def on_save_complete(success):
            if success and self.dashboard_callback:
                # Agendar notificação do dashboard na thread principal
                root.after(0, self.dashboard_callback)
        
        self.api_client.save_funcionarios(self.funcionarios, on_save_complete)
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