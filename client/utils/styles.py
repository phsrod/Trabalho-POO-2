"""
Configurações de estilos para a aplicação da barbearia
"""

import tkinter as tk
from tkinter import ttk

class StyleManager:
    """Gerenciador de estilos da aplicação"""
    
    # Cores do tema
    COLORS = {
        'primary': '#0078d4',      # Azul principal
        'primary_dark': '#106ebe', # Azul escuro
        'secondary': '#107c10',    # Verde
        'accent': '#ff8c00',       # Laranja
        'danger': '#d13438',       # Vermelho
        'warning': '#ffb900',      # Amarelo
        'success': '#107c10',      # Verde
        'info': '#0078d4',         # Azul
        'light': '#f8f9fa',        # Cinza claro
        'dark': '#343a40',         # Cinza escuro
        'white': '#ffffff',        # Branco
        'gray': '#6c757d',         # Cinza
        'border': '#dee2e6',       # Borda
    }
    
    @staticmethod
    def configure_styles():
        """Configura todos os estilos da aplicação"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Configurar estilos básicos
        StyleManager._configure_basic_styles(style)
        StyleManager._configure_button_styles(style)
        StyleManager._configure_frame_styles(style)
        StyleManager._configure_label_styles(style)
        StyleManager._configure_entry_styles(style)
        StyleManager._configure_treeview_styles(style)
        StyleManager._configure_combobox_styles(style)
    
    @staticmethod
    def _configure_basic_styles(style):
        """Configura estilos básicos"""
        # Frame principal
        style.configure('Main.TFrame', background=StyleManager.COLORS['light'])
        
        # Cards
        style.configure('Card.TFrame', 
                       background=StyleManager.COLORS['white'],
                       relief='solid',
                       borderwidth=1)
        
        # Frames de conteúdo
        style.configure('Content.TFrame', 
                       background=StyleManager.COLORS['white'],
                       relief='flat')
    
    @staticmethod
    def _configure_button_styles(style):
        """Configura estilos de botões"""
        # Botão primário
        style.configure('Primary.TButton',
                       background=StyleManager.COLORS['primary'],
                       foreground=StyleManager.COLORS['white'],
                       font=('Arial', 10, 'bold'),
                       padding=(12, 8),
                       relief='flat')
        
        style.map('Primary.TButton',
                 background=[('active', StyleManager.COLORS['primary_dark']),
                           ('pressed', StyleManager.COLORS['primary_dark'])])
        
        # Botão secundário
        style.configure('Secondary.TButton',
                       background=StyleManager.COLORS['secondary'],
                       foreground=StyleManager.COLORS['white'],
                       font=('Arial', 10, 'bold'),
                       padding=(12, 8),
                       relief='flat')
        
        # Botão de ação
        style.configure('Action.TButton',
                       background=StyleManager.COLORS['info'],
                       foreground=StyleManager.COLORS['white'],
                       font=('Arial', 9),
                       padding=(8, 4),
                       relief='flat')
        
        # Botão de perigo
        style.configure('Danger.TButton',
                       background=StyleManager.COLORS['danger'],
                       foreground=StyleManager.COLORS['white'],
                       font=('Arial', 9),
                       padding=(8, 4),
                       relief='flat')
        
        # Botão de menu
        style.configure('Menu.TButton',
               background=StyleManager.COLORS['primary'],  # azul base
               foreground=StyleManager.COLORS['white'],
               font=('Arial', 10),
               padding=(15, 8),
               relief='flat',
               borderwidth=0)

        # Mapeamento de estados
        style.map('Menu.TButton',
                background=[('active', StyleManager.COLORS['primary_dark']),
                            ('pressed', StyleManager.COLORS['primary_dark'])],
                foreground=[('active', StyleManager.COLORS['white']),
                            ('pressed', StyleManager.COLORS['white'])])
    
    @staticmethod
    def _configure_frame_styles(style):
        """Configura estilos de frames"""
        # Frame de cabeçalho
        style.configure('Header.TFrame',
                       background=StyleManager.COLORS['primary'],
                       relief='flat')
        
        # Frame de filtros
        style.configure('Filter.TFrame',
                       background=StyleManager.COLORS['white'],
                       relief='solid',
                       borderwidth=1)
        
        # Frame de lista
        style.configure('List.TFrame',
                       background=StyleManager.COLORS['white'],
                       relief='solid',
                       borderwidth=1)
    
    @staticmethod
    def _configure_label_styles(style):
        """Configura estilos de labels"""
        # Título principal
        style.configure('Title.TLabel',
                       font=('Arial', 16, 'bold'),
                       background=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['dark'])
        
        # Subtítulo
        style.configure('Subtitle.TLabel',
                       font=('Arial', 12),
                       background=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['gray'])
        
        # Label de estatística
        style.configure('Stat.TLabel',
                       font=('Arial', 24, 'bold'),
                       background=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['primary'])
        
        # Label de cabeçalho
        style.configure('Header.TLabel',
                       font=('Arial', 14, 'bold'),
                       background=StyleManager.COLORS['primary'],
                       foreground=StyleManager.COLORS['white'])
        
        # Label de campo
        style.configure('Field.TLabel',
                       font=('Arial', 10),
                       background=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['dark'])
    
    @staticmethod
    def _configure_entry_styles(style):
        """Configura estilos de campos de entrada"""
        # Entry padrão
        style.configure('Custom.TEntry',
                       fieldbackground=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['dark'],
                       font=('Arial', 10),
                       relief='solid',
                       borderwidth=1)
        
        # Entry focado
        style.map('Custom.TEntry',
                 fieldbackground=[('focus', StyleManager.COLORS['white'])],
                 bordercolor=[('focus', StyleManager.COLORS['primary'])])
    
    @staticmethod
    def _configure_treeview_styles(style):
        """Configura estilos de treeview"""
        # Treeview padrão
        style.configure('Custom.Treeview',
                       background=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['dark'],
                       font=('Arial', 10),
                       relief='flat',
                       borderwidth=0)
        
        # Cabeçalho do treeview
        style.configure('Custom.Treeview.Heading',
                       background=StyleManager.COLORS['light'],
                       foreground=StyleManager.COLORS['dark'],
                       font=('Arial', 10, 'bold'),
                       relief='flat',
                       borderwidth=1)
        
        # Linhas alternadas
        style.map('Custom.Treeview',
                 background=[('selected', StyleManager.COLORS['primary']),
                           ('!selected', StyleManager.COLORS['white'])],
                 foreground=[('selected', StyleManager.COLORS['white']),
                           ('!selected', StyleManager.COLORS['dark'])])
    
    @staticmethod
    def _configure_combobox_styles(style):
        """Configura estilos de combobox"""
        # Combobox padrão
        style.configure('Custom.TCombobox',
                       fieldbackground=StyleManager.COLORS['white'],
                       foreground=StyleManager.COLORS['dark'],
                       font=('Arial', 10),
                       relief='solid',
                       borderwidth=1)
        
        # Botão do combobox
        style.map('Custom.TCombobox',
                 fieldbackground=[('readonly', StyleManager.COLORS['white'])],
                 bordercolor=[('focus', StyleManager.COLORS['primary'])])
    
    @staticmethod
    def get_color(color_name):
        """Retorna uma cor pelo nome"""
        return StyleManager.COLORS.get(color_name, '#000000')
    
    @staticmethod
    def apply_card_style(widget):
        """Aplica estilo de card a um widget"""
        widget.configure(style='Card.TFrame')
    
    @staticmethod
    def apply_primary_button_style(widget):
        """Aplica estilo de botão primário a um widget"""
        widget.configure(style='Primary.TButton')
    
    @staticmethod
    def apply_title_style(widget):
        """Aplica estilo de título a um widget"""
        widget.configure(style='Title.TLabel')
