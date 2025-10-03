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

### 4. Criar um Superusuário (Opcional)

```bash
python manage.py createsuperuser
```

### 5. Iniciar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```
```

### 6. Acessar a Aplicação

O servidor estará disponível em `http://localhost:8000/`.

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
- O arquivo de banco de dados **não deve ser enviado para o GitHub**. Adicione `db.sqlite3` ao `.gitignore` se necessário.
- Para desenvolvimento, o SQLite é suficiente. Para produção, considere usar PostgreSQL ou MySQL.
