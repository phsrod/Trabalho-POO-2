import tkinter as tk
from tkinter import ttk, messagebox
from typing import List, Optional
from decimal import Decimal
from ..models import Servico
from ..repositories import get_api_client
from ..utils import bind_money_mask, bind_number_only, MoneyMask
from .loading_widget import LoadingWidget

class ServicosWidget:
    """Widget de gerenciamento de serviços para uso embutido"""
    
    def __init__(self, parent, dashboard_callback=None):
        self.parent = parent
        self.servicos: List[Servico] = []
        self.current_servico: Optional[Servico] = None
        self.api_client = get_api_client()
        self.dashboard_callback = dashboard_callback  # Callback para notificar dashboard
        self.loading_widget = None
        self.create_widget()
        self.load_data_from_file()
        # Não chamar refresh_servicos_list() aqui - será chamado quando os dados carregarem
    
    def load_data_from_file(self):
        """Carrega dados do banco de dados usando thread"""
        # Verificar se já tem cache e se a lista está vazia - se não tiver, mostrar loading
        if self.api_client._servicos is None and len(self.servicos) == 0:
            if self.loading_widget is None and hasattr(self, 'treeview_container'):
                # Esconder treeview temporariamente
                self.servicos_tree.pack_forget()
                # Mostrar loading no container
                self.loading_widget = LoadingWidget(self.treeview_container, "Carregando serviços")
                self.loading_widget.show()
        
        def on_data_loaded(servicos_loaded):
            # Agendar atualização da GUI na thread principal
            root = self.parent.winfo_toplevel()
            # Esconder loading e mostrar treeview
            if self.loading_widget:
                def hide_and_show():
                    self.loading_widget.hide()
                    self.servicos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
                root.after(0, hide_and_show)
            # Atualizar apenas se houver dados válidos (não None)
            if servicos_loaded is not None:
                self.servicos = servicos_loaded
                root.after(0, self.refresh_servicos_list)
            # Se servicos_loaded for None, manter dados antigos (não atualizar)
        
        # NÃO limpar lista - manter dados antigos visíveis até novos chegarem
        # Isso evita que a interface fique "nugada" durante carregamento
        # Carrega dados em thread (se já houver cache, será retornado imediatamente)
        self.api_client.load_servicos(on_data_loaded)
    
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
        
        # Treeview para lista de serviços
        columns = ('Nome', 'Preço', 'Duração', 'Status')
        self.servicos_tree = ttk.Treeview(self.treeview_container, columns=columns, show='headings', height=12)
        
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
        scrollbar = ttk.Scrollbar(self.treeview_container, orient=tk.VERTICAL, command=self.servicos_tree.yview)
        self.servicos_tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack treeview e scrollbar
        self.servicos_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
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
        bind_money_mask(self.preco_entry)
        
        # Duração
        ttk.Label(parent, text="Duração (min) *:").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.duracao_entry = ttk.Entry(parent, width=25, font=('Arial', 10))
        self.duracao_entry.grid(row=2, column=1, sticky=tk.W, padx=(10, 0), pady=5)
        bind_number_only(self.duracao_entry)
        
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
    
    def refresh_servicos_list(self):
        """Atualiza a lista de serviços"""
        # Verificar se o widget ainda existe
        try:
            if not hasattr(self, 'servicos_tree') or not self.servicos_tree.winfo_exists():
                return
        except:
            return
        
        # Limpar lista
        try:
            for item in self.servicos_tree.get_children():
                self.servicos_tree.delete(item)
        except:
            return
        
        # Obter termo de busca
        search_term = ""
        if hasattr(self, 'search_entry'):
            try:
                search_term = self.search_entry.get().strip().lower()
            except:
                pass
        
        # Adicionar serviços
        for servico in self.servicos:
            # Filtrar por busca se houver termo
            if search_term and search_term not in servico.nome.lower():
                continue
            
            status = "Ativo" if servico.ativo else "Inativo"
            # Formatar preço para exibição
            preco_formatado = MoneyMask.format_value(float(servico.preco))
            
            # Aplicar cor diferente para inativos
            tags = (servico.id,)
            if not servico.ativo:
                tags = (servico.id, 'inativo',)
            
            self.servicos_tree.insert('', 'end', values=(
                servico.nome,
                preco_formatado,
                servico.duracao_minutos,
                status
            ), tags=tags)
        
        # Configurar cor para inativos
        try:
            self.servicos_tree.tag_configure('inativo', foreground='gray')
        except:
            pass
    
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
        # Formatar preço como moeda
        self.preco_entry.insert(0, MoneyMask.format_value(float(servico.preco)))
        
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
        """Remove o serviço selecionado do banco de dados"""
        selection = self.servicos_tree.selection()
        if not selection:
            messagebox.showwarning("Aviso", "Selecione um serviço para excluir.")
            return
        
        item = self.servicos_tree.item(selection[0])
        servico_id = item['tags'][0] if item['tags'] else None
        
        if servico_id:
            servico = next((s for s in self.servicos if s.id == servico_id), None)
            if servico:
                if messagebox.askyesno("Confirmar", f"Deseja realmente EXCLUIR permanentemente o serviço {servico.nome}?\n\nEsta ação não pode ser desfeita!"):
                    root = self.parent.winfo_toplevel()
                    def on_delete_complete(success):
                        if success:
                            # Remover da lista local
                            self.servicos = [s for s in self.servicos if s.id != servico_id]
                            root.after(0, self.refresh_servicos_list)
                            root.after(0, self.clear_form)
                            root.after(0, lambda: messagebox.showinfo("Sucesso", "Serviço excluído permanentemente do banco de dados!"))
                            if self.dashboard_callback:
                                root.after(0, self.dashboard_callback)
                        else:
                            root.after(0, lambda: messagebox.showerror("Erro", "Erro ao excluir serviço. Tente novamente."))
                    
                    self.api_client.delete_servico(servico_id, on_delete_complete)
    
    def on_search_change(self):
        """Callback quando o campo de busca muda"""
        self.refresh_servicos_list()
    
    def clear_search(self):
        """Limpa o campo de busca"""
        if hasattr(self, 'search_entry'):
            self.search_entry.delete(0, tk.END)
            self.refresh_servicos_list()
    
    def save_servico(self):
        """Salva o serviço usando thread"""
        # Validar campos obrigatórios
        nome = self.nome_entry.get().strip()
        preco_str = self.preco_entry.get().strip()
        duracao_str = self.duracao_entry.get().strip()
        
        if not nome:
            messagebox.showerror("Erro", "Nome é obrigatório.")
            self.nome_entry.focus()
            return
        
        if not preco_str:
            messagebox.showerror("Erro", "Preço é obrigatório.")
            self.preco_entry.focus()
            return
        
        if not duracao_str:
            messagebox.showerror("Erro", "Duração é obrigatória.")
            self.duracao_entry.focus()
            return
        
        # Formatar campo monetário se ainda não estiver formatado
        if not preco_str.startswith('R$'):
            # Formata antes de extrair o valor
            formatted = MoneyMask.format_value_string(preco_str)
            if formatted:
                self.preco_entry.delete(0, tk.END)
                self.preco_entry.insert(0, formatted)
                preco_str = formatted
        
        try:
            # Extrair valor numérico do campo monetário
            preco = Decimal(str(MoneyMask.get_value(preco_str)))
            duracao = int(duracao_str)
            
            if preco < 0:
                messagebox.showerror("Erro", "O preço deve ser maior ou igual a zero.")
                self.preco_entry.focus()
                return
            
            if duracao <= 0:
                messagebox.showerror("Erro", "A duração deve ser maior que zero.")
                self.duracao_entry.focus()
                return
                
        except (ValueError, TypeError) as e:
            messagebox.showerror("Erro", f"Preço e duração devem ser números válidos.\n{str(e)}")
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
        
        # Salvar no banco de dados usando thread
        root = self.parent.winfo_toplevel()
        def on_save_complete(success):
            if success and self.dashboard_callback:
                # Agendar notificação do dashboard na thread principal
                root.after(0, self.dashboard_callback)
        
        self.api_client.save_servicos(self.servicos, on_save_complete)
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