# Configuração do Ambiente de Desenvolvimento com Docker

Este guia descreve como configurar e rodar o projeto `paperpaper` usando Docker e Docker Compose, incluindo o banco de dados PostgreSQL.

## Pré-requisitos

- **Docker**: Instale o [Docker Desktop](https://www.docker.com/products/docker-desktop/) para Windows, Linux ou macOS.
- **Git**: Necessário para clonar o repositório.

---

## Passo a Passo

### 1. Clonar o Repositório (se necessário)

Se você ainda não tem o projeto, clone o repositório do GitHub:

```bash
git clone git@github.com:HaniBR01/paperpaper.git
cd paperpaper
```

### 2. Configurar as Variáveis de Ambiente

Copie o arquivo `.env.example` para `.env` e ajuste as variáveis conforme necessário:

```bash
cp .env.example .env
# Edite o arquivo .env para definir usuário, senha e nome do banco, se desejar
```

### 3. Subir os Contêineres com Docker Compose

No diretório raiz do projeto, execute:

```bash
docker-compose up --build
```

O Docker irá:
- Baixar a imagem do PostgreSQL
- Construir a imagem da aplicação Django
- Subir ambos os serviços e garantir que eles possam se comunicar

### 4. Aplicar as Migrações do Banco de Dados

Abra um novo terminal e execute:

```bash
docker-compose exec web python manage.py migrate
```

### 5. Acessar a Aplicação

O servidor estará disponível em `http://localhost:8000/`.

---

## Comandos Úteis

- Parar os contêineres:
	```bash
	docker-compose down
	```
- Acessar o shell do Django:
	```bash
	docker-compose exec web python manage.py shell
	```
- Criar um superusuário:
	```bash
	docker-compose exec web python manage.py createsuperuser
	```

---

## Observações

- O banco de dados PostgreSQL terá seus dados persistidos no volume `postgres_data`.
- O arquivo `.env` **não deve ser enviado para o GitHub**. Use sempre o `.env.example` como referência.
