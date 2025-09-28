# Sistema Administrativo da Barbearia

Aplicação desktop desenvolvida em Python com Tkinter para gerenciamento administrativo de barbearia.

## Funcionalidades

### ✅ Implementadas
- **Sistema de Login**: Autenticação de administradores
- **Dashboard Principal**: Interface principal com estatísticas e navegação
- **Modelos de Dados**: Estruturas para Cliente, Serviço, Funcionário e Agendamento

### 🚧 Em Desenvolvimento
- Gerenciamento de Clientes
- Gerenciamento de Serviços
- Gerenciamento de Funcionários
- Visualização de Agendamentos
- Relatórios e Estatísticas
- Configurações do Sistema

## Estrutura do Projeto

```
Trabalho01POO/
├── gui/                    # Interface gráfica
│   ├── __init__.py
│   ├── login.py           # Tela de login
│   └── home.py            # Dashboard principal
├── models/                 # Modelos de dados
│   ├── __init__.py
│   ├── cliente.py         # Modelo Cliente
│   ├── servico.py         # Modelo Serviço
│   ├── funcionario.py     # Modelo Funcionário
│   └── agendamento.py     # Modelo Agendamento
├── main.py                # Arquivo principal
├── requirements.txt       # Dependências
└── README.md             # Documentação
```

## Como Executar

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação
1. Clone ou baixe o projeto
2. Navegue até a pasta do projeto
3. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```

### Execução
```bash
python main.py
```

## Credenciais de Acesso

**Usuário:** admin  
**Senha:** admin123

## Tecnologias Utilizadas

- **Python 3.x**: Linguagem de programação
- **Tkinter**: Framework para interface gráfica
- **Pillow**: Biblioteca para manipulação de imagens
- **Dataclasses**: Para definição dos modelos de dados

## Arquitetura

A aplicação segue o padrão MVC (Model-View-Controller):

- **Models**: Definem a estrutura dos dados (Cliente, Serviço, etc.)
- **Views**: Interfaces gráficas (login.py, home.py)
- **Controllers**: Lógica de negócio (implementada nas views por simplicidade)

## Próximos Passos

1. Implementar telas de gerenciamento para cada entidade
2. Adicionar persistência de dados (banco de dados)
3. Implementar validações e tratamento de erros
4. Adicionar relatórios e estatísticas
5. Melhorar a interface visual e UX

## Desenvolvido por

Sistema desenvolvido para a disciplina de Programação Orientada a Objetos 2.