# Sistema Administrativo da Barbearia

Sistema desktop para gerenciamento administrativo de barbearia com arquitetura cliente-servidor e padrão MVC.

## Estrutura do Projeto

```
projeto/
├── server/              # Servidor Flask (API REST)
│   ├── routes/         # Rotas da API
│   └── utils/          # Utilitários do servidor
├── client/             # Cliente Desktop (Tkinter)
│   ├── models/         # Modelos de domínio
│   ├── views/          # Interface gráfica (GUI)
│   ├── controllers/    # Controladores (lógica de negócio)
│   ├── repositories/   # Cliente API (acesso a dados)
│   └── utils/          # Utilitários do cliente
├── shared/             # Código compartilhado
│   └── database/       # Modelos e configuração de banco
└── data/               # Banco de dados SQLite
```

## Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## Instalação

1. Clone ou baixe o projeto
2. Navegue até a pasta do projeto
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

## Execução

**IMPORTANTE:** É necessário executar o servidor antes da aplicação!

1. **Primeiro, inicie o servidor Flask:**
   ```bash
   python server.py
   ```
   O servidor será iniciado em `http://localhost:5000`. Mantenha este terminal aberto.

2. **Em outro terminal, execute a aplicação:**
   ```bash
   python main.py
   ```

## Credenciais de Acesso

**Usuário:** admin  
**Senha:** admin123

## Arquitetura e Infraestrutura

### Visão Geral

O sistema utiliza uma arquitetura **cliente-servidor** com separação clara de responsabilidades seguindo o padrão **MVC (Model-View-Controller)**. A comunicação entre cliente e servidor é realizada através de uma **API REST** usando HTTP/JSON.

### Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────────┐
│                         CLIENTE (Desktop)                        │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    CAMADA DE APRESENTAÇÃO                │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │   │
│  │  │  Login   │  │  Home    │  │ Clientes │  │ Serviços │ │   │
│  │  │  Window  │  │  Window  │  │  Widget  │  │  Widget  │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐               │   │
│  │  │Funcionários│ │Agendamentos│ │Relatórios│               │   │
│  │  │  Widget   │  │   Widget   │  │  Widget  │               │   │
│  │  └──────────┘  └──────────┘  └──────────┘               │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│  ┌────────────────────────┼──────────────────────────────────┐  │
│  │              CAMADA DE CONTROLE (Controller)               │  │
│  │         ┌──────────────────────────────────────┐          │  │
│  │         │      BarbeariaApp (App Controller)   │          │  │
│  │         │  - Gerencia ciclo de vida da app     │          │  │
│  │         │  - Coordena navegação entre telas    │          │  │
│  │         └──────────────────────────────────────┘          │  │
│  └────────────────────────┼──────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────┼──────────────────────────────────┐  │
│  │         CAMADA DE MODELOS (Domain Models)                  │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐  │  │
│  │  │ Cliente  │  │Funcionário│ │ Serviço  │  │Agendamento│  │  │
│  │  │ (dataclass)│ │(dataclass)│ │(dataclass)│  │(dataclass)│  │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘  │  │
│  └────────────────────────┼──────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────┼──────────────────────────────────┐  │
│  │      CAMADA DE REPOSITÓRIO (Repository Pattern)          │  │
│  │         ┌──────────────────────────────────────┐          │  │
│  │         │         ApiClient                     │          │  │
│  │         │  - Gerencia cache local               │          │  │
│  │         │  - Faz requisições HTTP ao servidor   │          │  │
│  │         │  - Thread-safe operations             │          │  │
│  │         └──────────────────────────────────────┘          │  │
│  └────────────────────────┼──────────────────────────────────┘  │
└───────────────────────────┼──────────────────────────────────────┘
                            │
                    HTTP/JSON (REST API)
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    SERVIDOR (Flask API)                          │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │                    CAMADA DE ROTAS                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │   │
│  │  │ /clientes│  │/funcionarios│ │/servicos│  │/agendamentos│ │   │
│  │  │  (GET,   │  │  (GET, POST,│ │ (GET,   │  │  (GET,   │ │   │
│  │  │  POST,   │  │  DELETE)   │ │  POST,  │  │  POST)   │ │   │
│  │  │  DELETE) │  └──────────┘  │  DELETE) │  └──────────┘ │   │
│  │  └──────────┘                 └──────────┘                │   │
│  └──────────────────────────────────────────────────────────┘   │
│                           │                                      │
│  ┌────────────────────────┼──────────────────────────────────┐  │
│  │              CAMADA DE CONVERSÃO                          │  │
│  │         ┌──────────────────────────────────────┐          │  │
│  │         │      Converters (utils)              │          │  │
│  │         │  - Converte ORM → Dict → JSON        │          │  │
│  │         └──────────────────────────────────────┘          │  │
│  └────────────────────────┼──────────────────────────────────┘  │
│                           │                                      │
│  ┌────────────────────────┼──────────────────────────────────┐  │
│  │         CAMADA DE ACESSO A DADOS (ORM)                    │  │
│  │         ┌──────────────────────────────────────┐          │  │
│  │         │      SQLAlchemy ORM                   │          │  │
│  │         │  - ClienteDB, FuncionarioDB,          │          │  │
│  │         │    ServicoDB, AgendamentoDB           │          │  │
│  │         └──────────────────────────────────────┘          │  │
│  └────────────────────────┼──────────────────────────────────┘  │
└───────────────────────────┼──────────────────────────────────────┘
                            │
┌───────────────────────────┼──────────────────────────────────────┐
│                    BANCO DE DADOS                                │
│  ┌──────────────────────────────────────────────────────────┐   │
│  │              SQLite (barbearia.db)                       │   │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐ │   │
│  │  │ clientes │  │funcionarios│ │ servicos │  │agendamentos│ │   │
│  │  │  (table) │  │  (table)  │ │  (table) │  │  (table) │ │   │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘ │   │
│  └──────────────────────────────────────────────────────────┘   │
└──────────────────────────────────────────────────────────────────┘
```

### Componentes da Arquitetura

#### 1. Cliente (Desktop Application)

**Camada de Apresentação (Views)**
- **LoginWindow**: Tela de autenticação
- **HomeWindow**: Dashboard principal com estatísticas
- **Widgets Especializados**: ClientesWidget, ServicosWidget, FuncionariosWidget, AgendamentosWidget, RelatoriosWidget
- Responsável pela interface gráfica e interação com o usuário

**Camada de Controle (Controllers)**
- **BarbeariaApp**: Controlador principal que gerencia o ciclo de vida da aplicação
- Coordena a navegação entre telas
- Gerencia eventos e callbacks

**Camada de Modelos (Models)**
- **Cliente, Funcionario, Servico, Agendamento**: Modelos de domínio (dataclasses)
- Representam as entidades de negócio
- Possuem métodos `to_dict()` e `from_dict()` para serialização

**Camada de Repositório (Repositories)**
- **ApiClient**: Cliente HTTP que se comunica com o servidor
- Gerencia cache local para melhor performance
- Operações thread-safe para não bloquear a interface
- Implementa métodos CRUD via HTTP

#### 2. Servidor (Flask API)

**Camada de Rotas (Routes)**
- Endpoints REST para cada entidade:
  - `GET /api/clientes` - Lista todos os clientes
  - `POST /api/clientes` - Salva/atualiza clientes
  - `DELETE /api/clientes/<id>` - Remove cliente
  - Similar para funcionários, serviços e agendamentos
- `GET /api/health` - Health check do servidor

**Camada de Conversão (Utils)**
- Funções `*_to_dict()` que convertem objetos SQLAlchemy para dicionários JSON
- Garante serialização correta de tipos (datetime, Decimal, etc.)

**Camada de Acesso a Dados (ORM)**
- **SQLAlchemy ORM**: Mapeamento objeto-relacional
- Modelos: `ClienteDB`, `FuncionarioDB`, `ServicoDB`, `AgendamentoDB`
- Gerencia sessões de banco de dados
- Implementa relacionamentos entre entidades

#### 3. Banco de Dados

- **SQLite**: Banco de dados relacional local
- Armazenado em `data/barbearia.db`
- Tabelas criadas automaticamente via SQLAlchemy
- Suporta soft-delete (campo `ativo`)

### Fluxo de Dados

1. **Usuário interage com a interface** → View captura evento
2. **View chama Controller** → Controller processa ação
3. **Controller usa Repository** → ApiClient faz requisição HTTP
4. **Servidor recebe requisição** → Rota processa
5. **Rota usa ORM** → Consulta/atualiza banco de dados
6. **Resposta JSON** → Retorna ao cliente
7. **ApiClient atualiza cache** → View atualiza interface

### Padrões de Design Utilizados

- **MVC (Model-View-Controller)**: Separação de responsabilidades
- **Repository Pattern**: Abstração de acesso a dados
- **Client-Server**: Arquitetura distribuída
- **REST API**: Comunicação padronizada via HTTP
- **ORM (Object-Relational Mapping)**: Abstração de banco de dados

## Tutorial de Uso

### 1. Primeiro Acesso

1. **Inicie o servidor** (obrigatório antes de usar a aplicação):
   ```bash
   python server.py
   ```
   Aguarde a mensagem: "Servidor iniciando em http://localhost:5000"

2. **Inicie a aplicação** em outro terminal:
   ```bash
   python main.py
   ```

3. **Faça login**:
   - Usuário: `admin`
   - Senha: `admin123`
   - Clique em "Entrar"

### 2. Dashboard Administrativo

Após o login, você verá o **Dashboard** com:
- **Total de Clientes**: Contador de clientes ativos
- **Agendamentos Hoje**: Quantidade de agendamentos do dia
- **Receita Mensal**: Soma dos agendamentos concluídos do mês
- **Funcionários Ativos**: Contador de funcionários ativos

O dashboard atualiza automaticamente a cada 30 segundos e após operações.

### 3. Gerenciamento de Clientes

**Acessar**: Clique no botão "Clientes" no menu superior

**Funcionalidades**:
- **Buscar**: Digite o nome no campo de busca para filtrar
- **Novo Cliente**: Clique em "Novo" e preencha:
  - Nome* (obrigatório)
  - Telefone* (obrigatório, formato automático)
  - Email (validação automática)
  - Observações
  - Marque/desmarque "Cliente Ativo" para ativar/desativar
- **Editar**: Selecione um cliente na lista e clique em "Editar"
- **Excluir**: Selecione um cliente e clique em "Excluir" (remoção permanente)
- **Salvar**: Após preencher/editar, clique em "Salvar"

**Dicas**:
- Clientes inativos aparecem em cinza na lista
- Use a busca para encontrar clientes rapidamente
- O telefone é formatado automaticamente: (XX) XXXXX-XXXX

### 4. Gerenciamento de Serviços

**Acessar**: Clique no botão "Serviços" no menu superior

**Funcionalidades**:
- **Buscar**: Digite o nome do serviço para filtrar
- **Novo Serviço**: Clique em "Novo" e preencha:
  - Nome* (obrigatório)
  - Descrição
  - Preço* (formato monetário automático)
  - Duração em minutos
  - Marque/desmarque "Serviço Ativo"
- **Editar**: Selecione um serviço e clique em "Editar"
- **Excluir**: Selecione e clique em "Excluir" (remoção permanente)
- **Salvar**: Clique em "Salvar" após preencher

**Dicas**:
- O preço aceita valores monetários (ex: 25.50)
- Serviços inativos aparecem em cinza

### 5. Gerenciamento de Funcionários

**Acessar**: Clique no botão "Funcionários" no menu superior

**Funcionalidades**:
- **Buscar**: Digite o nome para filtrar
- **Novo Funcionário**: Clique em "Novo" e preencha:
  - Nome* (obrigatório)
  - Telefone* (obrigatório)
  - Email
  - Cargo
  - Salário (formato monetário)
  - Marque/desmarque "Funcionário Ativo"
- **Editar**: Selecione e clique em "Editar"
- **Excluir**: Selecione e clique em "Excluir" (remoção permanente)
- **Salvar**: Clique em "Salvar"

**Dicas**:
- A data de admissão é preenchida automaticamente
- Funcionários inativos aparecem em cinza

### 6. Agendamentos

**Acessar**: Clique no botão "Agendamentos" no menu superior

**Funcionalidades**:
- **Visualizar**: Lista todos os agendamentos com:
  - Cliente, Funcionário, Serviço
  - Data e horário
  - Status (agendado, confirmado, em_andamento, concluido, cancelado)
  - Valor total
- **Filtros**: Use os campos de data para filtrar agendamentos
- **Status**: Visualize o status atual de cada agendamento

**Dicas**:
- Os agendamentos são exibidos em ordem cronológica
- Use os filtros de data para encontrar agendamentos específicos

### 7. Relatórios e Estatísticas

**Acessar**: Clique no botão "Relatórios" no menu superior

**Funcionalidades**:
- **Estatísticas Gerais**:
  - Total de clientes, funcionários, serviços
  - Agendamentos por período
  - Receita por período
- **Filtros de Período**: Selecione data inicial e final
- **Exportar Relatório**: Clique em "Exportar Relatório" para gerar arquivo TXT
  - O arquivo será salvo no formato: `relatorio_barbearia_YYYYMMDD_HHMMSS.txt`

**Dicas**:
- Use os filtros de data para análises específicas
- Os relatórios incluem todas as informações relevantes do período

### 8. Navegação e Interface

- **Menu Superior**: Use os botões para navegar entre seções
- **Botão "✕"**: Aparece quando uma seção está aberta, clique para fechar
- **Dashboard**: Sempre visível no topo, atualiza automaticamente
- **Busca**: Disponível em Clientes, Serviços e Funcionários
- **Ativo/Inativo**: Use a checkbox para ativar/desativar registros sem excluir

### 9. Dicas Importantes

- **Servidor**: Sempre mantenha o servidor rodando enquanto usa a aplicação
- **Salvamento**: Clique em "Salvar" após fazer alterações
- **Exclusão**: A exclusão é permanente - use com cuidado
- **Ativo/Inativo**: Use a checkbox para desativar temporariamente sem perder dados
- **Busca**: Funciona em tempo real enquanto você digita
- **Dashboard**: Atualiza automaticamente após operações (100ms de delay)

### 10. Solução de Problemas

**Servidor não disponível**:
- Verifique se o servidor está rodando (`python server.py`)
- Confirme que está na porta 5000
- Reinicie o servidor se necessário

**Dados não aparecem**:
- Verifique a conexão com o servidor
- Aguarde alguns segundos para o carregamento
- Use o botão de busca para verificar se os dados existem

**Erro ao salvar**:
- Verifique se todos os campos obrigatórios estão preenchidos
- Confirme que o servidor está respondendo
- Verifique os logs do servidor para mais detalhes

## Funcionalidades

- ✅ Gerenciamento de Clientes (CRUD completo)
- ✅ Gerenciamento de Funcionários (CRUD completo)
- ✅ Gerenciamento de Serviços (CRUD completo)
- ✅ Agendamentos (visualização e gerenciamento)
- ✅ Relatórios e Estatísticas
- ✅ Exportação de relatórios em TXT
- ✅ Busca em tempo real (Clientes, Serviços, Funcionários)
- ✅ Dashboard com estatísticas em tempo real
- ✅ Sistema de ativação/desativação (soft-delete)
- ✅ Validação de campos (telefone, email, valores monetários)
- ✅ Interface responsiva e moderna
