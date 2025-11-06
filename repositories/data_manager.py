"""
Sistema de Gerenciamento de Dados com Persistência em Arquivos e Threads
Gerencia o carregamento, salvamento e exportação de dados usando threads
para manter a interface responsiva
"""

import json
import os
import threading
from typing import List, Optional, Callable
from datetime import datetime, date
from pathlib import Path
from models import Cliente, Funcionario, Servico, Agendamento

class DataManager:
    """Gerenciador de dados com persistência em arquivos JSON"""
    
    def __init__(self, data_dir: str = "data"):
        """
        Inicializa o gerenciador de dados
        
        Args:
            data_dir: Diretório onde os arquivos serão salvos
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        
        # Arquivos de dados
        self.clientes_file = self.data_dir / "clientes.json"
        self.funcionarios_file = self.data_dir / "funcionarios.json"
        self.servicos_file = self.data_dir / "servicos.json"
        self.agendamentos_file = self.data_dir / "agendamentos.json"
        
        # Lock para operações thread-safe
        self.lock = threading.Lock()
        
        # Cache de dados
        self._clientes: Optional[List[Cliente]] = None
        self._funcionarios: Optional[List[Funcionario]] = None
        self._servicos: Optional[List[Servico]] = None
        self._agendamentos: Optional[List[Agendamento]] = None
    
    def _safe_load_json(self, file_path: Path) -> list:
        """
        Carrega JSON de forma segura, tratando arquivos vazios ou corrompidos
        
        Args:
            file_path: Caminho do arquivo JSON
            
        Returns:
            Lista de dados (vazia se arquivo não existe, está vazio ou corrompido)
        """
        if not file_path.exists():
            return []
        
        # Verificar se o arquivo está vazio
        try:
            if file_path.stat().st_size == 0:
                print(f"Arquivo {file_path.name} está vazio. Inicializando como lista vazia.")
                return []
        except OSError:
            # Se não conseguir verificar o tamanho, tenta ler mesmo assim
            pass
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()
                # Verificar se o conteúdo está vazio após remover espaços
                if not content:
                    print(f"Arquivo {file_path.name} está vazio. Inicializando como lista vazia.")
                    return []
                
                data = json.loads(content)
                # Garantir que retorna uma lista
                if not isinstance(data, list):
                    print(f"Arquivo {file_path.name} não contém uma lista válida. Inicializando como lista vazia.")
                    return []
                
                return data
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar JSON do arquivo {file_path.name}: {e}")
            print(f"Arquivo corrompido. Inicializando como lista vazia.")
            return []
        except Exception as e:
            print(f"Erro ao ler arquivo {file_path.name}: {e}")
            return []
    
    def load_clientes(self, callback: Optional[Callable] = None) -> List[Cliente]:
        """
        Carrega clientes do arquivo em thread separada
        
        Args:
            callback: Função chamada após carregar (recebe lista de clientes)
        
        Returns:
            Lista de clientes (pode estar vazia se arquivo não existe)
        """
        def _load():
            try:
                with self.lock:
                    if self._clientes is not None:
                        if callback:
                            callback(self._clientes)
                        return self._clientes
                    
                    data = self._safe_load_json(self.clientes_file)
                    self._clientes = [Cliente.from_dict(item) for item in data]
                    
                    if callback:
                        callback(self._clientes)
                    return self._clientes
            except Exception as e:
                print(f"Erro ao carregar clientes: {e}")
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
        Salva clientes no arquivo em thread separada usando escrita atômica
        
        Args:
            clientes: Lista de clientes para salvar
            callback: Função chamada após salvar (recebe True se sucesso, False se erro)
        """
        def _save():
            try:
                with self.lock:
                    data = [cliente.to_dict() for cliente in clientes]
                    # Usar arquivo temporário para escrita atômica
                    temp_file = self.clientes_file.with_suffix('.tmp')
                    try:
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        # Renomear arquivo temporário para o arquivo final (operação atômica)
                        temp_file.replace(self.clientes_file)
                        self._clientes = clientes
                        if callback:
                            callback(True)
                    except Exception as e:
                        # Se houver erro, tentar remover arquivo temporário
                        if temp_file.exists():
                            try:
                                temp_file.unlink()
                            except:
                                pass
                        raise e
            except Exception as e:
                print(f"Erro ao salvar clientes: {e}")
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_funcionarios(self, callback: Optional[Callable] = None) -> List[Funcionario]:
        """Carrega funcionários do arquivo em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._funcionarios is not None:
                        if callback:
                            callback(self._funcionarios)
                        return self._funcionarios
                    
                    data = self._safe_load_json(self.funcionarios_file)
                    self._funcionarios = [Funcionario.from_dict(item) for item in data]
                    
                    if callback:
                        callback(self._funcionarios)
                    return self._funcionarios
            except Exception as e:
                print(f"Erro ao carregar funcionários: {e}")
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
        """Salva funcionários no arquivo em thread separada"""
        def _save():
            try:
                with self.lock:
                    data = [funcionario.to_dict() for funcionario in funcionarios]
                    # Usar arquivo temporário para escrita atômica
                    temp_file = self.funcionarios_file.with_suffix('.tmp')
                    try:
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        # Renomear arquivo temporário para o arquivo final (operação atômica)
                        temp_file.replace(self.funcionarios_file)
                        self._funcionarios = funcionarios
                        if callback:
                            callback(True)
                    except Exception as e:
                        # Se houver erro, tentar remover arquivo temporário
                        if temp_file.exists():
                            try:
                                temp_file.unlink()
                            except:
                                pass
                        raise e
            except Exception as e:
                print(f"Erro ao salvar funcionários: {e}")
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_servicos(self, callback: Optional[Callable] = None) -> List[Servico]:
        """Carrega serviços do arquivo em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._servicos is not None:
                        if callback:
                            callback(self._servicos)
                        return self._servicos
                    
                    data = self._safe_load_json(self.servicos_file)
                    self._servicos = [Servico.from_dict(item) for item in data]
                    
                    if callback:
                        callback(self._servicos)
                    return self._servicos
            except Exception as e:
                print(f"Erro ao carregar serviços: {e}")
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
        """Salva serviços no arquivo em thread separada"""
        def _save():
            try:
                with self.lock:
                    data = [servico.to_dict() for servico in servicos]
                    # Usar arquivo temporário para escrita atômica
                    temp_file = self.servicos_file.with_suffix('.tmp')
                    try:
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        # Renomear arquivo temporário para o arquivo final (operação atômica)
                        temp_file.replace(self.servicos_file)
                        self._servicos = servicos
                        if callback:
                            callback(True)
                    except Exception as e:
                        # Se houver erro, tentar remover arquivo temporário
                        if temp_file.exists():
                            try:
                                temp_file.unlink()
                            except:
                                pass
                        raise e
            except Exception as e:
                print(f"Erro ao salvar serviços: {e}")
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_agendamentos(self, callback: Optional[Callable] = None, force_reload: bool = False) -> List[Agendamento]:
        """Carrega agendamentos do arquivo em thread separada"""
        def _load():
            try:
                with self.lock:
                    # Se force_reload for True, ignora o cache
                    if self._agendamentos is not None and not force_reload:
                        if callback:
                            callback(self._agendamentos)
                        return self._agendamentos
                    
                    data = self._safe_load_json(self.agendamentos_file)
                    self._agendamentos = [Agendamento.from_dict(item) for item in data]
                    
                    if callback:
                        callback(self._agendamentos)
                    return self._agendamentos
            except Exception as e:
                print(f"Erro ao carregar agendamentos: {e}")
                import traceback
                traceback.print_exc()
                self._agendamentos = []
                if callback:
                    callback([])
                return []
        
        # Sempre carrega do arquivo na primeira vez
        if self._agendamentos is None or force_reload:
            thread = threading.Thread(target=_load, daemon=True)
            thread.start()
            return []
        
        if callback:
            callback(self._agendamentos)
        return self._agendamentos
    
    def save_agendamentos(self, agendamentos: List[Agendamento], callback: Optional[Callable] = None):
        """Salva agendamentos no arquivo em thread separada usando escrita atômica"""
        def _save():
            try:
                with self.lock:
                    data = [agendamento.to_dict() for agendamento in agendamentos]
                    # Usar arquivo temporário para escrita atômica
                    temp_file = self.agendamentos_file.with_suffix('.tmp')
                    try:
                        with open(temp_file, 'w', encoding='utf-8') as f:
                            json.dump(data, f, indent=2, ensure_ascii=False)
                        # Renomear arquivo temporário para o arquivo final (operação atômica)
                        temp_file.replace(self.agendamentos_file)
                        # Atualiza o cache com os novos dados
                        self._agendamentos = agendamentos
                        if callback:
                            callback(True)
                    except Exception as e:
                        # Se houver erro, tentar remover arquivo temporário
                        if temp_file.exists():
                            try:
                                temp_file.unlink()
                            except:
                                pass
                        raise e
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

