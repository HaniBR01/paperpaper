# Configuração do Ambiente de Desenvolvimento

Este guia descreve os passos para configurar o ambiente de desenvolvimento do projeto `paperpaper` em sistemas Windows e Linux/macOS.

## Pré-requisitos

- **Python 3.8+**: Certifique-se de que o Python está instalado. Você pode verificar a versão com o comando `python --version` ou `python3 --version`.
- **Git**: Necessário para clonar o repositório.

---

## Passo a Passo

### 1. Clonar o Repositório (se necessário)

Se você ainda não tem o projeto, clone o repositório do GitHub:

```bash
git clone <URL_DO_REPOSITORIO>
cd paperpaper
```

### 2. Criar o Ambiente Virtual

Dentro da pasta raiz do projeto, crie um ambiente virtual chamado `.venv`. Este comando é o mesmo para Windows e Linux.

```bash
python -m venv .venv
```

### 3. Ativar o Ambiente Virtual

A ativação é diferente dependendo do seu sistema operacional.

#### No Windows (PowerShell):

```powershell
# Pode ser necessário liberar a execução de scripts na primeira vez
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process

# Ativar
.venv\Scripts\Activate.ps1
```

#### No Linux ou macOS (Bash/Zsh):

```bash
source .venv/bin/activate
```

**Importante:** Após a ativação, você verá `(.venv)` no início do seu prompt de comando, indicando que o ambiente virtual está ativo.

### 4. Instalar as Dependências

Com o ambiente virtual ativo, instale todas as bibliotecas necessárias listadas no arquivo `requirements.txt`.

```bash
pip install -r requirements.txt
```

### 5. Aplicar as Migrações do Banco de Dados

Este comando configura o banco de dados inicial (SQLite) com as tabelas necessárias para o Django.

```bash
python manage.py migrate
```

### 6. Iniciar o Servidor de Desenvolvimento

Para rodar a aplicação localmente, use o comando:

```bash
python manage.py runserver
```

O servidor estará disponível em `http://127.0.0.1:8000/`.

---

## Resumo dos Comandos

<details>
<summary><strong>Windows (PowerShell)</strong></summary>

```powershell
# 1. Criar ambiente
python -m venv .venv

# 2. Ativar
.venv\Scripts\Activate.ps1

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar migrações
python manage.py migrate

# 5. Iniciar servidor
python manage.py runserver
```

</details>

<details>
<summary><strong>Linux / macOS (Bash/Zsh)</strong></summary>

```bash
# 1. Criar ambiente
python3 -m venv .venv

# 2. Ativar
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar migrações
python3 manage.py migrate

# 5. Iniciar servidor
python3 manage.py runserver
```
</details>
