from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Cliente:
    """Modelo para representar um cliente da barbearia"""
    id: Optional[int] = None
    nome: str = ""
    telefone: str = ""
    email: str = ""
    data_cadastro: Optional[datetime] = None
    observacoes: str = ""
    ativo: bool = True
    
    def __post_init__(self):
        if self.data_cadastro is None:
            self.data_cadastro = datetime.now()
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'telefone': self.telefone,
            'email': self.email,
            'data_cadastro': self.data_cadastro.isoformat() if self.data_cadastro else None,
            'observacoes': self.observacoes,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Cliente':
        """Cria um objeto Cliente a partir de um dicionário"""
        data_cadastro = None
        if data.get('data_cadastro'):
            data_cadastro = datetime.fromisoformat(data['data_cadastro'])
        
        return cls(
            id=data.get('id'),
            nome=data.get('nome', ''),
            telefone=data.get('telefone', ''),
            email=data.get('email', ''),
            data_cadastro=data_cadastro,
            observacoes=data.get('observacoes', ''),
            ativo=data.get('ativo', True)
        )
