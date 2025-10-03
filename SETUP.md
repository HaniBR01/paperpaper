# Configuração do Ambiente de Desenvolvimento com Conda

Este guia descreve como configurar e rodar o projeto `paperpaper` usando Conda e SQLite.

## Pré-requisitos

- **Conda**: Instale o [Miniconda](https://docs.conda.io/en/latest/miniconda.html) ou [Anaconda](https://www.anaconda.com/products/distribution)
- **Git**: Necessário para clonar o repositório.

---

## Passo a Passo

### 1. Clonar o Repositório (se necessário)

Se você ainda não tem o projeto, clone o repositório do GitHub:

```bash
git clone git@github.com:HaniBR01/paperpaper.git
cd paperpaper
```

### 2. Criar o Ambiente Conda

Crie e ative o ambiente conda usando o arquivo `environment.yml`:

```bash
conda env create -f environment.yml
conda activate paperpaper
```

### 3. Aplicar as Migrações do Banco de Dados

```bash
python manage.py migrate
```

### 4. Criar um Superusuário

```bash
python manage.py createsuperuser
```

### 5. Configurar Permissões do Sistema (Opcional)

Para configurar grupos de usuários e permissões automaticamente:

```bash
python manage.py shell < setup_permissions.py
```

Este comando criará:
- **Grupo "Administradores"**: Acesso total ao sistema
- **Grupo "Usuários"**: Apenas visualização

### 6. Iniciar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```
```

### 7. Acessar a Aplicação

O servidor estará disponível em `http://localhost:8000/`.

**Para acessar o painel administrativo:**
- URL: `http://localhost:8000/admin/`
- Use as credenciais do superusuário criado

---

## Gerenciamento de Usuários e Permissões

### Atribuir usuários aos grupos:

1. Acesse o Django Admin (`http://localhost:8000/admin/`)
2. Vá em **"Usuários"** → Selecione um usuário
3. Na seção **"Grupos"**, adicione o usuário ao grupo desejado:
   - **Administradores**: Para usuários com acesso total
   - **Usuários**: Para usuários com acesso apenas de visualização

### Criar novos usuários:

1. No Django Admin, vá em **"Usuários"** → **"Adicionar usuário"**
2. Preencha username e senha
3. Após salvar, edite o usuário para adicionar informações extras
4. Atribua ao grupo apropriado

---

## Comandos Úteis

- **Desativar o ambiente conda:**
  ```bash
  conda deactivate
  ```

- **Reativar o ambiente:**
  ```bash
  conda activate paperpaper
  ```

- **Atualizar dependências:**
  ```bash
  conda env update -f environment.yml
  ```

- **Configurar permissões do sistema:**
  ```bash
  python manage.py shell < setup_permissions.py
  ```

- **Acessar o shell do Django:**
  ```bash
  python manage.py shell
  ```

- **Executar testes:**
  ```bash
  python manage.py test
  ```

- **Coletar arquivos estáticos:**
  ```bash
  python manage.py collectstatic
  ```

---

## Observações

- O banco de dados SQLite será criado automaticamente como `db.sqlite3` na raiz do projeto.
- O banco de dados **está incluído no repositório** para facilitar o desenvolvimento colaborativo.
- Para desenvolvimento, o SQLite é suficiente. Para produção, considere usar PostgreSQL ou MySQL.
- Execute o script de permissões sempre que configurar um novo ambiente ou resetar o banco de dados.
