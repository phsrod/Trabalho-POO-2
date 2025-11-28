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

## Arquitetura

- **MVC (Model-View-Controller)**: Separação clara de responsabilidades
- **Cliente-Servidor**: Comunicação via API REST
- **Repository Pattern**: Abstração de acesso a dados
- **SQLite**: Banco de dados local

## Funcionalidades

- Gerenciamento de Clientes
- Gerenciamento de Funcionários
- Gerenciamento de Serviços
- Agendamentos
- Relatórios e Estatísticas
- Exportação de relatórios em TXT
