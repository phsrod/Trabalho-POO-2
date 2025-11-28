from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from decimal import Decimal

@dataclass
class Agendamento:
    """Modelo para representar um agendamento de serviço"""
    id: Optional[int] = None
    cliente_id: int = 0
    funcionario_id: int = 0
    servico_id: int = 0
    data_agendamento: Optional[datetime] = None
    horario_inicio: Optional[datetime] = None
    horario_fim: Optional[datetime] = None
    status: str = "agendado"  # agendado, confirmado, em_andamento, concluido, cancelado
    observacoes: str = ""
    valor_total: Decimal = Decimal('0.00')
    
    def to_dict(self) -> dict:
        """Converte o objeto para dicionário"""
        return {
            'id': self.id,
            'cliente_id': self.cliente_id,
            'funcionario_id': self.funcionario_id,
            'servico_id': self.servico_id,
            'data_agendamento': self.data_agendamento.isoformat() if self.data_agendamento else None,
            'horario_inicio': self.horario_inicio.isoformat() if self.horario_inicio else None,
            'horario_fim': self.horario_fim.isoformat() if self.horario_fim else None,
            'status': self.status,
            'observacoes': self.observacoes,
            'valor_total': float(self.valor_total)
        }
    
    @classmethod
    def from_dict(cls, data: dict) -> 'Agendamento':
        """Cria um objeto Agendamento a partir de um dicionário"""
        data_agendamento = None
        if data.get('data_agendamento'):
            try:
                # Tenta parsear como datetime completo
                data_agendamento = datetime.fromisoformat(data['data_agendamento'])
            except (ValueError, TypeError):
                try:
                    # Tenta parsear como apenas data (YYYY-MM-DD)
                    date_str = data['data_agendamento']
                    if isinstance(date_str, str) and 'T' not in date_str:
                        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
                        data_agendamento = datetime.combine(date_obj, datetime.min.time())
                except (ValueError, TypeError):
                    pass
        
        horario_inicio = None
        if data.get('horario_inicio'):
            try:
                horario_inicio = datetime.fromisoformat(data['horario_inicio'])
            except (ValueError, TypeError):
                pass
        
        horario_fim = None
        if data.get('horario_fim'):
            try:
                horario_fim = datetime.fromisoformat(data['horario_fim'])
            except (ValueError, TypeError):
                pass
        
        return cls(
            id=data.get('id'),
            cliente_id=data.get('cliente_id', 0),
            funcionario_id=data.get('funcionario_id', 0),
            servico_id=data.get('servico_id', 0),
            data_agendamento=data_agendamento,
            horario_inicio=horario_inicio,
            horario_fim=horario_fim,
            status=data.get('status', 'agendado'),
            observacoes=data.get('observacoes', ''),
            valor_total=Decimal(str(data.get('valor_total', 0.00)))
        )
