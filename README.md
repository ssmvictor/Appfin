# FinDash - Painel de Finanças Pessoais

O FinDash é uma aplicação web moderna e intuitiva para gerenciar suas finanças pessoais. Ele fornece uma visão clara da sua situação financeira, permitindo que você acompanhe suas contas, transações, orçamentos e relatórios com facilidade.

## Funcionalidades

- **Painel de Controle:** Um painel completo que exibe seu patrimônio líquido, dinheiro, dívidas, além de gráficos interativos de "Receitas vs. Despesas" e "Detalhamento de Despesas".
- **Gerenciamento de Transações:** Adicione, edite e exclua transações com descrições, valores, datas, contas e categorias.
- **Página de Relatórios:** Obtenha insights sobre seus gastos com um resumo mensal de receitas e despesas e um detalhamento de despesas por categoria.
- **Página de Configurações:** Gerencie suas contas e categorias de forma simples, com opções para adicionar, editar e excluir.
- **UI Moderna:** Uma interface de usuário limpa e moderna, traduzida para o português do Brasil.

## Estrutura do Projeto

- **`app.py`:** O arquivo principal da aplicação Flask. Ele gerencia as rotas, conexões com o banco de dados e serve o frontend.
- **`database.py`:** Contém os modelos de dados (`Account`, `Category`, `Transaction`) e a classe `Database`, que gerencia todas as interações com o banco de dados SQLite.
- **`templates/`:** A pasta que contém os templates Jinja2 para todas as páginas da aplicação (`index.html`, `transactions.html`, etc.).
- **`requirements.txt`:** Uma lista das dependências Python necessárias para executar o projeto.
- **`.gitignore`:** Um arquivo que especifica quais arquivos e diretórios devem ser ignorados pelo Git.

## Como Executar

1.  **Clone o repositório:**
    ```bash
    git clone <url-do-repositorio>
    cd <diretorio-do-repositorio>
    ```

2.  **Crie e ative um ambiente virtual:**
    ```bash
    python -m venv venv
    source venv/bin/activate  # No Windows, use `venv\Scripts\activate`
    ```

3.  **Instale as dependências:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Execute a aplicação:**
    ```bash
    flask run
    ```

    A aplicação estará disponível em `http://127.0.0.1:5000`.
