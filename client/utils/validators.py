"""
Módulo de Validação e Máscaras para Campos de Entrada
Fornece funções para aplicar máscaras e validar dados em formulários
"""

import re
import tkinter as tk
from typing import Callable, Optional


class PhoneMask:
    """Máscara para telefone brasileiro: (XX) XXXXX-XXXX ou (XX) XXXX-XXXX"""
    
    @staticmethod
    def apply(event: tk.Event) -> str:
        """Aplica máscara de telefone durante a digitação"""
        widget = event.widget
        value = widget.get()
        
        # Remove tudo que não é número
        numbers = re.sub(r'\D', '', value)
        
        # Limita a 11 dígitos (DDD + número)
        if len(numbers) > 11:
            numbers = numbers[:11]
        
        # Aplica a máscara
        if len(numbers) == 0:
            masked = ""
        elif len(numbers) <= 2:
            masked = f"({numbers}"
        elif len(numbers) <= 7:
            masked = f"({numbers[:2]}) {numbers[2:]}"
        elif len(numbers) <= 10:
            masked = f"({numbers[:2]}) {numbers[2:6]}-{numbers[6:]}"
        else:
            masked = f"({numbers[:2]}) {numbers[2:7]}-{numbers[7:]}"
        
        # Atualiza o campo
        if value != masked:
            widget.delete(0, tk.END)
            widget.insert(0, masked)
            widget.icursor(tk.END)
        
        return "break"
    
    @staticmethod
    def validate(value: str) -> bool:
        """Valida se o telefone está no formato correto"""
        numbers = re.sub(r'\D', '', value)
        return len(numbers) >= 10 and len(numbers) <= 11
    
    @staticmethod
    def get_numbers(value: str) -> str:
        """Retorna apenas os números do telefone"""
        return re.sub(r'\D', '', value)


class EmailValidator:
    """Validador e formatador de email"""
    
    @staticmethod
    def validate(email: str) -> bool:
        """Valida formato de email"""
        if not email or not email.strip():
            return True  # Email é opcional
        
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(pattern, email.strip()))
    
    @staticmethod
    def format(event: tk.Event) -> str:
        """Formata email em tempo real (remove espaços, converte para minúsculas)"""
        widget = event.widget
        value = widget.get()
        
        # Remove espaços e converte para minúsculas
        formatted = value.replace(' ', '').lower()
        
        if value != formatted:
            cursor_pos = widget.index(tk.INSERT)
            widget.delete(0, tk.END)
            widget.insert(0, formatted)
            # Tenta manter a posição do cursor
            try:
                widget.icursor(min(cursor_pos, len(formatted)))
            except:
                widget.icursor(tk.END)
        
        return "break"


class MoneyMask:
    """Máscara para valores monetários: R$ X.XXX,XX"""
    
    @staticmethod
    def _filter_input(event: tk.Event):
        """Filtra entrada para permitir números, vírgula e ponto"""
        # Permite teclas de controle
        if event.keysym in ['BackSpace', 'Delete', 'Left', 'Right', 'Home', 'End', 'Tab', 'Return']:
            return None
        
        # Permite Ctrl+A, Ctrl+C, Ctrl+V, Ctrl+X
        if event.state & 0x4:  # Control key
            return None
        
        # Permite números, vírgula e ponto
        if event.char and event.char not in '0123456789,.':
            return "break"
        
        return None
    
    @staticmethod
    def apply(event: tk.Event):
        """Não formata durante a digitação, apenas valida"""
        # Não faz nada durante a digitação para não interferir
        return None
    
    @staticmethod
    def format_value_string(value: str) -> str:
        """Formata uma string de valor monetário para o formato R$ X.XXX,XX"""
        if not value or not value.strip():
            return ""
        
        value = value.strip()
        
        # Se já está formatado (começa com R$), retorna como está
        if value.startswith('R$'):
            return value
        
        try:
            # Remove espaços
            clean_value = value.replace(' ', '')
            
            # Verifica se tem vírgula ou ponto (separador decimal)
            has_comma = ',' in clean_value
            has_dot = '.' in clean_value
            
            if has_comma or has_dot:
                # Tem separador decimal
                if has_comma:
                    # Vírgula como separador decimal (formato brasileiro)
                    # Remove pontos (milhares) e substitui vírgula por ponto
                    parts = clean_value.split(',')
                    if len(parts) == 2:
                        # Tem vírgula decimal
                        integer_part = parts[0].replace('.', '')
                        decimal_part = parts[1][:2]  # Máximo 2 casas decimais
                        amount = float(f"{integer_part}.{decimal_part}")
                    else:
                        # Vírgula como separador de milhares (formato inválido, trata como decimal)
                        amount = float(clean_value.replace('.', '').replace(',', '.'))
                else:
                    # Ponto como separador decimal (formato internacional)
                    # Remove outros pontos (milhares) e mantém apenas o último
                    parts = clean_value.split('.')
                    if len(parts) == 2:
                        # Tem ponto decimal
                        integer_part = parts[0].replace(',', '')
                        decimal_part = parts[1][:2]  # Máximo 2 casas decimais
                        amount = float(f"{integer_part}.{decimal_part}")
                    else:
                        # Múltiplos pontos (milhares), mantém apenas o último como decimal
                        integer_part = ''.join(parts[:-1]).replace(',', '')
                        decimal_part = parts[-1][:2]
                        amount = float(f"{integer_part}.{decimal_part}")
            else:
                # Não tem separador decimal - trata como valor inteiro em reais
                # Ex: "100" = R$ 100,00 (não R$ 1,00)
                amount = float(clean_value)
            
            # Formata como moeda brasileira
            return f"R$ {amount:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
        except (ValueError, OverflowError):
            # Se não conseguiu parsear, retorna string vazia
            return ""
    
    @staticmethod
    def _format_on_focus_out(event: tk.Event):
        """Formata o valor ao perder o foco"""
        widget = event.widget
        value = widget.get().strip()
        
        # Se está vazio, não faz nada
        if not value:
            return
        
        # Se já está formatado (começa com R$), não faz nada
        if value.startswith('R$'):
            return
        
        formatted = MoneyMask.format_value_string(value)
        if formatted:
            widget.delete(0, tk.END)
            widget.insert(0, formatted)
    
    @staticmethod
    def get_value(value: str) -> float:
        """Retorna o valor numérico do campo monetário"""
        if not value or not value.strip():
            return 0.0
        
        value = value.strip()
        
        # Se já está formatado (começa com R$), remove o prefixo
        if value.startswith('R$'):
            value = value[2:].strip()
        
        # Remove espaços
        value = value.replace(' ', '')
        
        if not value:
            return 0.0
        
        # Verifica se tem vírgula ou ponto
        has_comma = ',' in value
        has_dot = '.' in value
        
        try:
            if has_comma and has_dot:
                # Tem ambos: vírgula é decimal, ponto é milhar (formato brasileiro)
                # Ex: "1.234,56"
                value = value.replace('.', '').replace(',', '.')
                return float(value)
            elif has_comma:
                # Só tem vírgula: pode ser decimal ou milhar
                # Se tem mais de uma vírgula, é inválido, trata como decimal
                if value.count(',') == 1:
                    # Uma vírgula: assume que é decimal (formato brasileiro)
                    value = value.replace(',', '.')
                    return float(value)
                else:
                    # Múltiplas vírgulas: inválido
                    return 0.0
            elif has_dot:
                # Só tem ponto: pode ser decimal ou milhar
                parts = value.split('.')
                if len(parts) == 2:
                    # Um ponto: assume que é decimal (formato internacional)
                    return float(value)
                else:
                    # Múltiplos pontos: assume que são milhares, último é decimal
                    # Ex: "1.234.56" -> "1234.56"
                    integer_part = ''.join(parts[:-1])
                    decimal_part = parts[-1]
                    return float(f"{integer_part}.{decimal_part}")
            else:
                # Não tem separador: número inteiro
                return float(value)
        except (ValueError, TypeError):
            return 0.0
    
    @staticmethod
    def format_value(value: float) -> str:
        """Formata um valor float como moeda brasileira"""
        return f"R$ {value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')


class DateMask:
    """Máscara para data: DD/MM/AAAA"""
    
    @staticmethod
    def apply(event: tk.Event) -> str:
        """Aplica máscara de data durante a digitação"""
        widget = event.widget
        value = widget.get()
        
        # Remove tudo que não é número
        numbers = re.sub(r'\D', '', value)
        
        # Limita a 8 dígitos
        if len(numbers) > 8:
            numbers = numbers[:8]
        
        # Aplica a máscara
        if len(numbers) == 0:
            masked = ""
        elif len(numbers) <= 2:
            masked = numbers
        elif len(numbers) <= 4:
            masked = f"{numbers[:2]}/{numbers[2:]}"
        else:
            masked = f"{numbers[:2]}/{numbers[2:4]}/{numbers[4:]}"
        
        # Validação básica
        if len(numbers) >= 2:
            day = int(numbers[:2])
            if day > 31:
                masked = f"31/{masked[3:]}" if len(numbers) > 2 else "31"
                numbers = "31" + numbers[2:]
        
        if len(numbers) >= 4:
            month = int(numbers[2:4])
            if month > 12:
                masked = f"{masked[:3]}12/{masked[6:]}" if len(numbers) > 4 else f"{masked[:3]}12"
                numbers = numbers[:2] + "12" + numbers[4:]
        
        # Atualiza o campo
        if value != masked:
            widget.delete(0, tk.END)
            widget.insert(0, masked)
            widget.icursor(tk.END)
        
        return "break"
    
    @staticmethod
    def validate(value: str) -> bool:
        """Valida se a data está no formato correto"""
        pattern = r'^\d{2}/\d{2}/\d{4}$'
        if not re.match(pattern, value):
            return False
        
        try:
            day, month, year = map(int, value.split('/'))
            if day < 1 or day > 31 or month < 1 or month > 12 or year < 1900 or year > 2100:
                return False
            return True
        except ValueError:
            return False


class TimeMask:
    """Máscara para hora: HH:MM"""
    
    @staticmethod
    def apply(event: tk.Event) -> str:
        """Aplica máscara de hora durante a digitação"""
        widget = event.widget
        value = widget.get()
        
        # Remove tudo que não é número
        numbers = re.sub(r'\D', '', value)
        
        # Limita a 4 dígitos
        if len(numbers) > 4:
            numbers = numbers[:4]
        
        # Aplica a máscara
        if len(numbers) == 0:
            masked = ""
        elif len(numbers) <= 2:
            masked = numbers
        else:
            masked = f"{numbers[:2]}:{numbers[2:]}"
        
        # Validação básica
        if len(numbers) >= 2:
            hour = int(numbers[:2])
            if hour > 23:
                masked = f"23:{masked[3:]}" if len(numbers) > 2 else "23"
                numbers = "23" + numbers[2:]
        
        if len(numbers) >= 4:
            minute = int(numbers[2:4])
            if minute > 59:
                masked = f"{masked[:3]}59"
                numbers = numbers[:2] + "59"
        
        # Atualiza o campo
        if value != masked:
            widget.delete(0, tk.END)
            widget.insert(0, masked)
            widget.icursor(tk.END)
        
        return "break"
    
    @staticmethod
    def validate(value: str) -> bool:
        """Valida se a hora está no formato correto"""
        pattern = r'^\d{2}:\d{2}$'
        if not re.match(pattern, value):
            return False
        
        try:
            hour, minute = map(int, value.split(':'))
            if hour < 0 or hour > 23 or minute < 0 or minute > 59:
                return False
            return True
        except ValueError:
            return False


class NumberOnlyValidator:
    """Validador que permite apenas números"""
    
    @staticmethod
    def apply(event: tk.Event) -> str:
        """Permite apenas números"""
        char = event.char
        if char and not char.isdigit():
            return "break"
        return None


def bind_phone_mask(entry: tk.Entry):
    """Aplica máscara de telefone a um Entry"""
    entry.bind('<KeyRelease>', PhoneMask.apply)
    entry.bind('<FocusOut>', lambda e: _validate_phone(e))


def bind_email_validator(entry: tk.Entry):
    """Aplica validação de email a um Entry"""
    entry.bind('<KeyRelease>', EmailValidator.format)
    entry.bind('<FocusOut>', lambda e: _validate_email(e))


def bind_money_mask(entry: tk.Entry):
    """Aplica máscara monetária a um Entry"""
    # Filtra entrada para permitir apenas números
    entry.bind('<KeyPress>', MoneyMask._filter_input)
    # Formata apenas ao perder o foco
    entry.bind('<FocusOut>', MoneyMask._format_on_focus_out)
    entry.bind('<FocusIn>', lambda e: _select_all_on_focus(e))


def bind_date_mask(entry: tk.Entry):
    """Aplica máscara de data a um Entry"""
    entry.bind('<KeyRelease>', DateMask.apply)


def bind_time_mask(entry: tk.Entry):
    """Aplica máscara de hora a um Entry"""
    entry.bind('<KeyRelease>', TimeMask.apply)


def bind_number_only(entry: tk.Entry):
    """Aplica validação de apenas números a um Entry"""
    entry.bind('<KeyPress>', NumberOnlyValidator.apply)


def _validate_phone(event: tk.Event):
    """Valida telefone ao perder o foco"""
    widget = event.widget
    value = widget.get()
    if value and not PhoneMask.validate(value):
        # Se não está válido mas tem conteúdo, mantém (pode ser editado depois)
        pass


def _validate_email(event: tk.Event):
    """Valida email ao perder o foco"""
    widget = event.widget
    value = widget.get()
    if value and not EmailValidator.validate(value):
        # Muda a cor da borda para indicar erro (se possível)
        try:
            widget.config(highlightcolor='red', highlightbackground='red')
        except:
            pass


def _select_all_on_focus(event: tk.Event):
    """Seleciona todo o texto ao receber foco (útil para campos monetários)"""
    widget = event.widget
    widget.select_range(0, tk.END)
    widget.icursor(tk.END)

