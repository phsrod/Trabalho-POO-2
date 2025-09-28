from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Funcionario:
    """Modelo para representar um funcionário da barbearia"""
    id: Optional[int] = None
    nome: str = ""
    telefone: str = ""
    email: str = ""
    cargo: str = ""
    data_admissao: Optional[datetime] = None
    salario: float = 0.0
    ativo: bool = True
    
    def __post_init__(self):
        if self.data_admissao is None:
            self.data_admissao = datetime.now()
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'cargo': self.cargo,
            'data_admissao': self.data_admissao.isoformat() if self.data_admissao else None,
            'salario': self.salario,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Funcionario':
        """Cria um objeto Funcionario a partir de um dicionário"""
        data_admissao = None
        if data.get('data_admissao'):
            data_admissao = datetime.fromisoformat(data['data_admissao'])
        
        return cls(
            id=data.get('id'),
            nome=data.get('nome', ''),
            telefone=data.get('telefone', ''),
            email=data.get('email', ''),
            cargo=data.get('cargo', ''),
            data_admissao=data_admissao,
            salario=data.get('salario', 0.0),
            ativo=data.get('ativo', True)
        )
