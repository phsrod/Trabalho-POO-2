"""
Sistema de Gerenciamento de Dados com Persistência em Banco de Dados
Gerencia o carregamento, salvamento e exportação de dados usando threads
para manter a interface responsiva
"""

import threading
from typing import List, Optional, Callable
from datetime import datetime, date
from decimal import Decimal
from models import Cliente, Funcionario, Servico, Agendamento
from .database import SessionLocal, init_db
from .db_models import ClienteDB, FuncionarioDB, ServicoDB, AgendamentoDB

class DataManager:
    """Gerenciador de dados com persistência em banco de dados SQLite"""
    
    def __init__(self):
        """Inicializa o gerenciador de dados e cria as tabelas se não existirem"""
        # Inicializar banco de dados
        init_db()
        
        # Lock para operações thread-safe
        self.lock = threading.Lock()
        
        # Cache de dados
        self._clientes: Optional[List[Cliente]] = None
        self._funcionarios: Optional[List[Funcionario]] = None
        self._servicos: Optional[List[Servico]] = None
        self._agendamentos: Optional[List[Agendamento]] = None
    
    def _db_to_cliente(self, db_obj: ClienteDB) -> Cliente:
        """Converte ClienteDB para Cliente"""
        return Cliente(
            id=db_obj.id,
            nome=db_obj.nome,
            telefone=db_obj.telefone,
            email=db_obj.email,
            data_cadastro=db_obj.data_cadastro,
            observacoes=db_obj.observacoes,
            ativo=db_obj.ativo
        )
    
    def _cliente_to_db(self, cliente: Cliente, db_obj: Optional[ClienteDB] = None) -> ClienteDB:
        """Converte Cliente para ClienteDB"""
        if db_obj is None:
            db_obj = ClienteDB()
        
        db_obj.nome = cliente.nome
        db_obj.telefone = cliente.telefone
        db_obj.email = cliente.email
        db_obj.data_cadastro = cliente.data_cadastro or datetime.now()
        db_obj.observacoes = cliente.observacoes
        db_obj.ativo = cliente.ativo
        
        return db_obj
    
    def _db_to_funcionario(self, db_obj: FuncionarioDB) -> Funcionario:
        """Converte FuncionarioDB para Funcionario"""
        return Funcionario(
            id=db_obj.id,
            nome=db_obj.nome,
            telefone=db_obj.telefone,
            email=db_obj.email,
            cargo=db_obj.cargo,
            data_admissao=db_obj.data_admissao,
            salario=db_obj.salario,
            ativo=db_obj.ativo
        )
    
    def _funcionario_to_db(self, funcionario: Funcionario, db_obj: Optional[FuncionarioDB] = None) -> FuncionarioDB:
        """Converte Funcionario para FuncionarioDB"""
        if db_obj is None:
            db_obj = FuncionarioDB()
        
        db_obj.nome = funcionario.nome
        db_obj.telefone = funcionario.telefone
        db_obj.email = funcionario.email
        db_obj.cargo = funcionario.cargo
        db_obj.data_admissao = funcionario.data_admissao or datetime.now()
        db_obj.salario = funcionario.salario
        db_obj.ativo = funcionario.ativo
        
        return db_obj
    
    def _db_to_servico(self, db_obj: ServicoDB) -> Servico:
        """Converte ServicoDB para Servico"""
        return Servico(
            id=db_obj.id,
            nome=db_obj.nome,
            descricao=db_obj.descricao,
            preco=Decimal(str(db_obj.preco)),
            duracao_minutos=db_obj.duracao_minutos,
            ativo=db_obj.ativo
        )
    
    def _servico_to_db(self, servico: Servico, db_obj: Optional[ServicoDB] = None) -> ServicoDB:
        """Converte Servico para ServicoDB"""
        if db_obj is None:
            db_obj = ServicoDB()
        
        db_obj.nome = servico.nome
        db_obj.descricao = servico.descricao
        db_obj.preco = float(servico.preco)
        db_obj.duracao_minutos = servico.duracao_minutos
        db_obj.ativo = servico.ativo
        
        return db_obj
    
    def _db_to_agendamento(self, db_obj: AgendamentoDB) -> Agendamento:
        """Converte AgendamentoDB para Agendamento"""
        return Agendamento(
            id=db_obj.id,
            cliente_id=db_obj.cliente_id,
            funcionario_id=db_obj.funcionario_id,
            servico_id=db_obj.servico_id,
            data_agendamento=db_obj.data_agendamento,
            horario_inicio=db_obj.horario_inicio,
            horario_fim=db_obj.horario_fim,
            status=db_obj.status,
            observacoes=db_obj.observacoes,
            valor_total=Decimal(str(db_obj.valor_total))
        )
    
    def _agendamento_to_db(self, agendamento: Agendamento, db_obj: Optional[AgendamentoDB] = None) -> AgendamentoDB:
        """Converte Agendamento para AgendamentoDB"""
        if db_obj is None:
            db_obj = AgendamentoDB()
        
        db_obj.cliente_id = agendamento.cliente_id
        db_obj.funcionario_id = agendamento.funcionario_id
        db_obj.servico_id = agendamento.servico_id
        db_obj.data_agendamento = agendamento.data_agendamento
        db_obj.horario_inicio = agendamento.horario_inicio
        db_obj.horario_fim = agendamento.horario_fim
        db_obj.status = agendamento.status
        db_obj.observacoes = agendamento.observacoes
        db_obj.valor_total = float(agendamento.valor_total)
        
        return db_obj
    
    def load_clientes(self, callback: Optional[Callable] = None) -> List[Cliente]:
        """
        Carrega clientes do banco de dados em thread separada
        
        Args:
            callback: Função chamada após carregar (recebe lista de clientes)
        
        Returns:
            Lista de clientes (pode estar vazia se não houver dados)
        """
        def _load():
            try:
                with self.lock:
                    if self._clientes is not None:
                        if callback:
                            callback(self._clientes)
                        return self._clientes
                    
                    db = SessionLocal()
                    try:
                        db_clientes = db.query(ClienteDB).all()
                        self._clientes = [self._db_to_cliente(c) for c in db_clientes]
                        
                        if callback:
                            callback(self._clientes)
                        return self._clientes
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao carregar clientes: {e}")
                import traceback
                traceback.print_exc()
                self._clientes = []
                if callback:
                    callback([])
                return []
        
        # Se já está em cache, retorna imediatamente
        if self._clientes is not None:
            if callback:
                callback(self._clientes)
            return self._clientes
        
        # Caso contrário, carrega em thread
        thread = threading.Thread(target=_load, daemon=True)
        thread.start()
        return []
    
    def save_clientes(self, clientes: List[Cliente], callback: Optional[Callable] = None):
        """
        Salva clientes no banco de dados em thread separada
        
        Args:
            clientes: Lista de clientes para salvar
            callback: Função chamada após salvar (recebe True se sucesso, False se erro)
        """
        def _save():
            try:
                with self.lock:
                    db = SessionLocal()
                    try:
                        # Buscar todos os clientes existentes
                        existing_ids = {c.id for c in db.query(ClienteDB).all()}
                        clientes_dict = {c.id: c for c in clientes if c.id}
                        
                        # Atualizar ou criar clientes
                        for cliente in clientes:
                            if cliente.id and cliente.id in existing_ids:
                                # Atualizar existente
                                db_cliente = db.query(ClienteDB).filter(ClienteDB.id == cliente.id).first()
                                if db_cliente:
                                    self._cliente_to_db(cliente, db_cliente)
                            else:
                                # Criar novo
                                db_cliente = self._cliente_to_db(cliente)
                                db.add(db_cliente)
                                # Atualizar o ID do cliente após inserção
                                db.flush()
                                cliente.id = db_cliente.id
                        
                        # Remover clientes que não estão mais na lista
                        current_ids = {c.id for c in clientes if c.id}
                        to_remove = existing_ids - current_ids
                        if to_remove:
                            db.query(ClienteDB).filter(ClienteDB.id.in_(to_remove)).delete(synchronize_session=False)
                        
                        db.commit()
                        self._clientes = clientes
                        
                        if callback:
                            callback(True)
                    except Exception as e:
                        db.rollback()
                        raise e
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao salvar clientes: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_funcionarios(self, callback: Optional[Callable] = None) -> List[Funcionario]:
        """Carrega funcionários do banco de dados em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._funcionarios is not None:
                        if callback:
                            callback(self._funcionarios)
                        return self._funcionarios
                    
                    db = SessionLocal()
                    try:
                        db_funcionarios = db.query(FuncionarioDB).all()
                        self._funcionarios = [self._db_to_funcionario(f) for f in db_funcionarios]
                        
                        if callback:
                            callback(self._funcionarios)
                        return self._funcionarios
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao carregar funcionários: {e}")
                import traceback
                traceback.print_exc()
                self._funcionarios = []
                if callback:
                    callback([])
                return []
        
        if self._funcionarios is not None:
            if callback:
                callback(self._funcionarios)
            return self._funcionarios
        
        thread = threading.Thread(target=_load, daemon=True)
        thread.start()
        return []
    
    def save_funcionarios(self, funcionarios: List[Funcionario], callback: Optional[Callable] = None):
        """Salva funcionários no banco de dados em thread separada"""
        def _save():
            try:
                with self.lock:
                    db = SessionLocal()
                    try:
                        existing_ids = {f.id for f in db.query(FuncionarioDB).all()}
                        
                        for funcionario in funcionarios:
                            if funcionario.id and funcionario.id in existing_ids:
                                db_funcionario = db.query(FuncionarioDB).filter(FuncionarioDB.id == funcionario.id).first()
                                if db_funcionario:
                                    self._funcionario_to_db(funcionario, db_funcionario)
                            else:
                                db_funcionario = self._funcionario_to_db(funcionario)
                                db.add(db_funcionario)
                                db.flush()
                                funcionario.id = db_funcionario.id
                        
                        current_ids = {f.id for f in funcionarios if f.id}
                        to_remove = existing_ids - current_ids
                        if to_remove:
                            db.query(FuncionarioDB).filter(FuncionarioDB.id.in_(to_remove)).delete(synchronize_session=False)
                        
                        db.commit()
                        self._funcionarios = funcionarios
                        
                        if callback:
                            callback(True)
                    except Exception as e:
                        db.rollback()
                        raise e
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao salvar funcionários: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_servicos(self, callback: Optional[Callable] = None) -> List[Servico]:
        """Carrega serviços do banco de dados em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._servicos is not None:
                        if callback:
                            callback(self._servicos)
                        return self._servicos
                    
                    db = SessionLocal()
                    try:
                        db_servicos = db.query(ServicoDB).all()
                        self._servicos = [self._db_to_servico(s) for s in db_servicos]
                        
                        if callback:
                            callback(self._servicos)
                        return self._servicos
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao carregar serviços: {e}")
                import traceback
                traceback.print_exc()
                self._servicos = []
                if callback:
                    callback([])
                return []
        
        if self._servicos is not None:
            if callback:
                callback(self._servicos)
            return self._servicos
        
        thread = threading.Thread(target=_load, daemon=True)
        thread.start()
        return []
    
    def save_servicos(self, servicos: List[Servico], callback: Optional[Callable] = None):
        """Salva serviços no banco de dados em thread separada"""
        def _save():
            try:
                with self.lock:
                    db = SessionLocal()
                    try:
                        existing_ids = {s.id for s in db.query(ServicoDB).all()}
                        
                        for servico in servicos:
                            if servico.id and servico.id in existing_ids:
                                db_servico = db.query(ServicoDB).filter(ServicoDB.id == servico.id).first()
                                if db_servico:
                                    self._servico_to_db(servico, db_servico)
                            else:
                                db_servico = self._servico_to_db(servico)
                                db.add(db_servico)
                                db.flush()
                                servico.id = db_servico.id
                        
                        current_ids = {s.id for s in servicos if s.id}
                        to_remove = existing_ids - current_ids
                        if to_remove:
                            db.query(ServicoDB).filter(ServicoDB.id.in_(to_remove)).delete(synchronize_session=False)
                        
                        db.commit()
                        self._servicos = servicos
                        
                        if callback:
                            callback(True)
                    except Exception as e:
                        db.rollback()
                        raise e
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao salvar serviços: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_agendamentos(self, callback: Optional[Callable] = None, force_reload: bool = False) -> List[Agendamento]:
        """Carrega agendamentos do banco de dados em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._agendamentos is not None and not force_reload:
                        if callback:
                            callback(self._agendamentos)
                        return self._agendamentos
                    
                    db = SessionLocal()
                    try:
                        db_agendamentos = db.query(AgendamentoDB).all()
                        self._agendamentos = [self._db_to_agendamento(a) for a in db_agendamentos]
                        
                        if callback:
                            callback(self._agendamentos)
                        return self._agendamentos
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao carregar agendamentos: {e}")
                import traceback
                traceback.print_exc()
                self._agendamentos = []
                if callback:
                    callback([])
                return []
        
        if self._agendamentos is None or force_reload:
            thread = threading.Thread(target=_load, daemon=True)
            thread.start()
            return []
        
        if callback:
            callback(self._agendamentos)
        return self._agendamentos
    
    def save_agendamentos(self, agendamentos: List[Agendamento], callback: Optional[Callable] = None):
        """Salva agendamentos no banco de dados em thread separada"""
        def _save():
            try:
                with self.lock:
                    db = SessionLocal()
                    try:
                        existing_ids = {a.id for a in db.query(AgendamentoDB).all()}
                        
                        for agendamento in agendamentos:
                            if agendamento.id and agendamento.id in existing_ids:
                                db_agendamento = db.query(AgendamentoDB).filter(AgendamentoDB.id == agendamento.id).first()
                                if db_agendamento:
                                    self._agendamento_to_db(agendamento, db_agendamento)
                            else:
                                db_agendamento = self._agendamento_to_db(agendamento)
                                db.add(db_agendamento)
                                db.flush()
                                agendamento.id = db_agendamento.id
                        
                        current_ids = {a.id for a in agendamentos if a.id}
                        to_remove = existing_ids - current_ids
                        if to_remove:
                            db.query(AgendamentoDB).filter(AgendamentoDB.id.in_(to_remove)).delete(synchronize_session=False)
                        
                        db.commit()
                        self._agendamentos = agendamentos
                        
                        if callback:
                            callback(True)
                    except Exception as e:
                        db.rollback()
                        raise e
                    finally:
                        db.close()
            except Exception as e:
                print(f"Erro ao salvar agendamentos: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def export_relatorio_txt(self, 
                            clientes: List[Cliente],
                            funcionarios: List[Funcionario],
                            servicos: List[Servico],
                            agendamentos: List[Agendamento],
                            data_inicial: datetime,
                            data_final: datetime,
                            output_file: str,
                            callback: Optional[Callable] = None):
        """
        Exporta relatório em formato TXT em thread separada
        
        Args:
            clientes: Lista de clientes
            funcionarios: Lista de funcionários
            servicos: Lista de serviços
            agendamentos: Lista de agendamentos
            data_inicial: Data inicial do período
            data_final: Data final do período
            output_file: Caminho do arquivo de saída
            callback: Função chamada após exportar (recebe True se sucesso, False se erro)
        """
        def _export():
            try:
                with self.lock:
                    # Filtrar agendamentos do período (apenas concluídos para relatórios)
                    agendamentos_periodo = []
                    data_inicial_date = data_inicial.date() if isinstance(data_inicial, datetime) else data_inicial
                    data_final_date = data_final.date() if isinstance(data_final, datetime) else data_final
                    
                    for a in agendamentos:
                        # Verificar status
                        if a.status != 'concluido':
                            continue
                        
                        # Verificar se tem data_agendamento
                        if not a.data_agendamento:
                            continue
                        
                        # Normalizar data_agendamento para date
                        try:
                            if isinstance(a.data_agendamento, datetime):
                                data_agendamento_date = a.data_agendamento.date()
                            elif isinstance(a.data_agendamento, date):
                                data_agendamento_date = a.data_agendamento
                            else:
                                continue
                            
                            # Verificar se está no período (garantir que ambos são date)
                            if isinstance(data_agendamento_date, date) and isinstance(data_inicial_date, date) and isinstance(data_final_date, date):
                                if data_inicial_date <= data_agendamento_date <= data_final_date:
                                    agendamentos_periodo.append(a)
                        except (AttributeError, TypeError, ValueError):
                            # Se houver erro na conversão, pular este agendamento
                            continue
                    
                    # Calcular estatísticas
                    receita_total = sum(float(a.valor_total) for a in agendamentos_periodo)
                    clientes_ativos = len([c for c in clientes if c.ativo])
                    funcionarios_ativos = len([f for f in funcionarios if f.ativo])
                    
                    # Gerar relatório
                    with open(output_file, 'w', encoding='utf-8') as f:
                        f.write("=" * 80 + "\n")
                        f.write("RELATÓRIO DE VENDAS - BARBEARIA\n")
                        f.write("=" * 80 + "\n\n")
                        f.write(f"Período: {data_inicial.strftime('%d/%m/%Y')} a {data_final.strftime('%d/%m/%Y')}\n")
                        f.write(f"Data de geração: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}\n\n")
                        
                        f.write("-" * 80 + "\n")
                        f.write("ESTATÍSTICAS GERAIS\n")
                        f.write("-" * 80 + "\n")
                        f.write(f"Total de Clientes Ativos: {clientes_ativos}\n")
                        f.write(f"Total de Funcionários Ativos: {funcionarios_ativos}\n")
                        f.write(f"Total de Agendamentos: {len(agendamentos_periodo)}\n")
                        f.write(f"Receita Total: R$ {receita_total:.2f}\n\n")
                        
                        # Relatório de serviços
                        from collections import defaultdict
                        servico_count = defaultdict(int)
                        servico_receita = defaultdict(float)
                        
                        for agendamento in agendamentos_periodo:
                            servico = next((s for s in servicos if s.id == agendamento.servico_id), None)
                            if servico:
                                servico_count[servico.nome] += 1
                                servico_receita[servico.nome] += float(agendamento.valor_total)
                        
                        f.write("-" * 80 + "\n")
                        f.write("SERVIÇOS MAIS POPULARES\n")
                        f.write("-" * 80 + "\n")
                        sorted_servicos = sorted(servico_count.items(), key=lambda x: x[1], reverse=True)
                        for servico_nome, quantidade in sorted_servicos:
                            receita = servico_receita[servico_nome]
                            f.write(f"{servico_nome:<40} | Qtd: {quantidade:>3} | Receita: R$ {receita:>10.2f}\n")
                        
                        f.write("\n")
                        
                        # Relatório de funcionários
                        funcionario_count = defaultdict(int)
                        funcionario_receita = defaultdict(float)
                        
                        for agendamento in agendamentos_periodo:
                            funcionario = next((f for f in funcionarios if f.id == agendamento.funcionario_id), None)
                            if funcionario:
                                funcionario_count[funcionario.nome] += 1
                                funcionario_receita[funcionario.nome] += float(agendamento.valor_total)
                        
                        f.write("-" * 80 + "\n")
                        f.write("PERFORMANCE DOS FUNCIONÁRIOS\n")
                        f.write("-" * 80 + "\n")
                        sorted_funcionarios = sorted(funcionario_count.items(), key=lambda x: x[1], reverse=True)
                        for funcionario_nome, quantidade in sorted_funcionarios:
                            receita = funcionario_receita[funcionario_nome]
                            f.write(f"{funcionario_nome:<40} | Agendamentos: {quantidade:>3} | Receita: R$ {receita:>10.2f}\n")
                        
                        f.write("\n" + "=" * 80 + "\n")
                        f.write("FIM DO RELATÓRIO\n")
                        f.write("=" * 80 + "\n")
                    
                    if callback:
                        callback(True, output_file)
            except Exception as e:
                print(f"Erro ao exportar relatório: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False, str(e))
        
        thread = threading.Thread(target=_export, daemon=True)
        thread.start()


# Instância global do gerenciador de dados
_data_manager = None

def get_data_manager() -> DataManager:
    """Retorna a instância global do gerenciador de dados"""
    global _data_manager
    if _data_manager is None:
        _data_manager = DataManager()
    return _data_manager
