"""
Cliente API REST
Gerencia comunicação com o servidor Flask via HTTP
"""

import threading
import requests
from typing import List, Optional, Callable
from datetime import datetime, date
from decimal import Decimal
from ..models import Cliente, Funcionario, Servico, Agendamento

# URL base do servidor
SERVER_URL = "http://localhost:5000"

class ApiClient:
    """Cliente API que se comunica com servidor Flask via HTTP"""
    
    def __init__(self, server_url: str = SERVER_URL):
        """
        Inicializa o gerenciador de dados
        
        Args:
            server_url: URL do servidor Flask (padrão: http://localhost:5000)
        """
        self.server_url = server_url
        
        # Lock para operações thread-safe
        self.lock = threading.Lock()
        
        # Cache de dados
        self._clientes: Optional[List[Cliente]] = None
        self._funcionarios: Optional[List[Funcionario]] = None
        self._servicos: Optional[List[Servico]] = None
        self._agendamentos: Optional[List[Agendamento]] = None
    
    def _check_server(self) -> bool:
        """Verifica se o servidor está rodando"""
        try:
            response = requests.get(f"{self.server_url}/api/health", timeout=2)
            return response.status_code == 200
        except:
            return False
    
    def load_clientes(self, callback: Optional[Callable] = None) -> List[Cliente]:
        """
        Carrega clientes do servidor em thread separada
        
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
                    
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        # NÃO seta cache como lista vazia - mantém None para tentar novamente
                        if callback:
                            callback([])
                        return []
                    
                    response = requests.get(f"{self.server_url}/api/clientes", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self._clientes = [Cliente.from_dict(item) for item in data]
                        if callback:
                            callback(self._clientes)
                        return self._clientes
                    else:
                        # Erro na requisição - não seta cache para permitir nova tentativa
                        if callback:
                            callback([])
                        return []
            except Exception as e:
                print(f"Erro ao carregar clientes: {e}")
                import traceback
                traceback.print_exc()
                # NÃO seta cache como lista vazia - mantém None para tentar novamente quando servidor voltar
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
        Salva clientes no servidor em thread separada
        
        Args:
            clientes: Lista de clientes para salvar
            callback: Função chamada após salvar (recebe True se sucesso, False se erro)
        """
        def _save():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        if callback:
                            callback(False)
                        return
                    
                    data = [cliente.to_dict() for cliente in clientes]
                    response = requests.post(
                        f"{self.server_url}/api/clientes",
                        json={'clientes': data},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            self._clientes = clientes
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
            except Exception as e:
                print(f"Erro ao salvar clientes: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_funcionarios(self, callback: Optional[Callable] = None) -> List[Funcionario]:
        """Carrega funcionários do servidor em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._funcionarios is not None:
                        if callback:
                            callback(self._funcionarios)
                        return self._funcionarios
                    
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        # NÃO seta cache como lista vazia - mantém None para tentar novamente
                        if callback:
                            callback([])
                        return []
                    
                    response = requests.get(f"{self.server_url}/api/funcionarios", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self._funcionarios = [Funcionario.from_dict(item) for item in data]
                        if callback:
                            callback(self._funcionarios)
                        return self._funcionarios
                    else:
                        # Erro na requisição - não seta cache para permitir nova tentativa
                        if callback:
                            callback([])
                        return []
            except Exception as e:
                print(f"Erro ao carregar funcionários: {e}")
                import traceback
                traceback.print_exc()
                # NÃO seta cache como lista vazia - mantém None para tentar novamente quando servidor voltar
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
        """Salva funcionários no servidor em thread separada"""
        def _save():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        if callback:
                            callback(False)
                        return
                    
                    data = [funcionario.to_dict() for funcionario in funcionarios]
                    response = requests.post(
                        f"{self.server_url}/api/funcionarios",
                        json={'funcionarios': data},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            self._funcionarios = funcionarios
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
            except Exception as e:
                print(f"Erro ao salvar funcionários: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def load_servicos(self, callback: Optional[Callable] = None) -> List[Servico]:
        """Carrega serviços do servidor em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._servicos is not None:
                        if callback:
                            callback(self._servicos)
                        return self._servicos
                    
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        # NÃO seta cache como lista vazia - mantém None para tentar novamente
                        if callback:
                            callback([])
                        return []
                    
                    response = requests.get(f"{self.server_url}/api/servicos", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self._servicos = [Servico.from_dict(item) for item in data]
                        if callback:
                            callback(self._servicos)
                        return self._servicos
                    else:
                        # Erro na requisição - não seta cache para permitir nova tentativa
                        if callback:
                            callback([])
                        return []
            except Exception as e:
                print(f"Erro ao carregar serviços: {e}")
                import traceback
                traceback.print_exc()
                # NÃO seta cache como lista vazia - mantém None para tentar novamente quando servidor voltar
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
        """Salva serviços no servidor em thread separada"""
        def _save():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        if callback:
                            callback(False)
                        return
                    
                    data = [servico.to_dict() for servico in servicos]
                    response = requests.post(
                        f"{self.server_url}/api/servicos",
                        json={'servicos': data},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            self._servicos = servicos
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
            except Exception as e:
                print(f"Erro ao salvar serviços: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_save, daemon=True)
        thread.start()
    
    def delete_cliente(self, cliente_id: int, callback: Optional[Callable] = None):
        """Remove um cliente do banco de dados"""
        def _delete():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando!")
                        if callback:
                            callback(False)
                        return
                    
                    response = requests.delete(
                        f"{self.server_url}/api/clientes/{cliente_id}",
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            # Limpar cache para forçar recarregamento
                            self._clientes = None
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
            except Exception as e:
                print(f"Erro ao deletar cliente: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_delete, daemon=True)
        thread.start()
    
    def delete_funcionario(self, funcionario_id: int, callback: Optional[Callable] = None):
        """Remove um funcionário do banco de dados"""
        def _delete():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando!")
                        if callback:
                            callback(False)
                        return
                    
                    response = requests.delete(
                        f"{self.server_url}/api/funcionarios/{funcionario_id}",
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            # Limpar cache para forçar recarregamento
                            self._funcionarios = None
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
            except Exception as e:
                print(f"Erro ao deletar funcionário: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_delete, daemon=True)
        thread.start()
    
    def delete_servico(self, servico_id: int, callback: Optional[Callable] = None):
        """Remove um serviço do banco de dados"""
        def _delete():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando!")
                        if callback:
                            callback(False)
                        return
                    
                    response = requests.delete(
                        f"{self.server_url}/api/servicos/{servico_id}",
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            # Limpar cache para forçar recarregamento
                            self._servicos = None
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
            except Exception as e:
                print(f"Erro ao deletar serviço: {e}")
                import traceback
                traceback.print_exc()
                if callback:
                    callback(False)
        
        thread = threading.Thread(target=_delete, daemon=True)
        thread.start()
    
    def load_agendamentos(self, callback: Optional[Callable] = None, force_reload: bool = False) -> List[Agendamento]:
        """Carrega agendamentos do servidor em thread separada"""
        def _load():
            try:
                with self.lock:
                    if self._agendamentos is not None and not force_reload:
                        if callback:
                            callback(self._agendamentos)
                        return self._agendamentos
                    
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        # NÃO seta cache como lista vazia - mantém None para tentar novamente
                        if callback:
                            callback([])
                        return []
                    
                    response = requests.get(f"{self.server_url}/api/agendamentos", timeout=10)
                    if response.status_code == 200:
                        data = response.json()
                        self._agendamentos = [Agendamento.from_dict(item) for item in data]
                        if callback:
                            callback(self._agendamentos)
                        return self._agendamentos
                    else:
                        # Erro na requisição - não seta cache para permitir nova tentativa
                        if callback:
                            callback([])
                        return []
            except Exception as e:
                print(f"Erro ao carregar agendamentos: {e}")
                import traceback
                traceback.print_exc()
                # NÃO seta cache como lista vazia - mantém None para tentar novamente quando servidor voltar
                if callback:
                    callback([])
                return []
        
        # Se force_reload, limpa o cache antes de recarregar
        if force_reload:
            self._agendamentos = None
        
        if self._agendamentos is None:
            thread = threading.Thread(target=_load, daemon=True)
            thread.start()
            return []
        
        if callback:
            callback(self._agendamentos)
        return self._agendamentos
    
    def save_agendamentos(self, agendamentos: List[Agendamento], callback: Optional[Callable] = None):
        """Salva agendamentos no servidor em thread separada"""
        def _save():
            try:
                with self.lock:
                    if not self._check_server():
                        print("ERRO: Servidor não está rodando! Execute 'python server.py' primeiro.")
                        if callback:
                            callback(False)
                        return
                    
                    data = [agendamento.to_dict() for agendamento in agendamentos]
                    response = requests.post(
                        f"{self.server_url}/api/agendamentos",
                        json={'agendamentos': data},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        if result.get('success'):
                            self._agendamentos = agendamentos
                            if callback:
                                callback(True)
                        else:
                            if callback:
                                callback(False)
                    else:
                        if callback:
                            callback(False)
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


# Instância global do cliente API
_api_client = None

def get_api_client() -> ApiClient:
    """Retorna a instância global do cliente API"""
    global _api_client
    if _api_client is None:
        _api_client = ApiClient()
    return _api_client
