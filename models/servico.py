from dataclasses import dataclass
from typing import Optional
from decimal import Decimal

@dataclass
class Servico:
    """Modelo para representar um serviço oferecido pela barbearia"""
    id: Optional[int] = None
    nome: str = ""
    descricao: str = ""
    preco: Decimal = Decimal('0.00')
    duracao_minutos: int = 30
    ativo: bool = True
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao,
            'preco': float(self.preco),
            'duracao_minutos': self.duracao_minutos,
            'ativo': self.ativo
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Servico':
        """Cria um objeto Servico a partir de um dicionário"""
        return cls(
            id=data.get('id'),
            nome=data.get('nome', ''),
            descricao=data.get('descricao', ''),
            preco=Decimal(str(data.get('preco', 0.00))),
            duracao_minutos=data.get('duracao_minutos', 30),
            ativo=data.get('ativo', True)
        )
