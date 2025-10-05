# PaperPaper - Sistema de Gerenciamento de Artigos Acadêmicos

## Visão Geral

O PaperPaper é um sistema web desenvolvido em Django para gerenciamento e catalogação de artigos acadêmicos de eventos científicos. O sistema permite organizar eventos, edições, artigos e autores, oferecendo funcionalidades tanto para administradores quanto para usuários finais.

## Resumo da Implementação

O sistema foi implementado como um projeto Django monolítico, centralizando todas as funcionalidades no app principal `paperpaper`. A arquitetura segue os padrões MVT (Model-View-Template) do Django e atende completamente aos 8 testes de aceitação especificados.

## Arquitetura do Sistema

### Estrutura de Modelos (Models)

#### Core Models
- **`Event`**: Eventos acadêmicos (SBES, SBCARS, etc.)
  - Campos: `name`, `acronym`, `promoting_entity`, `slug`
  - Relacionamento: 1:N com Edition
  
- **`Edition`**: Edições específicas dos eventos
  - Campos: `event` (FK), `year`, `location`
  - Constraint: Unicidade por evento/ano
  
- **`Article`**: Artigos acadêmicos
  - Campos: `title`, `edition` (FK), `start_page`, `end_page`, `pdf_file`, `bibtex_key`, `slug`
  - Relacionamento: M:N com Author
  
- **`Author`**: Autores dos artigos
  - Campos: `full_name`, `slug`
  - Relacionamento: M:N com Article

#### Supporting Models
- **`NotificationSubscription`**: Inscrições para notificações por email
  - Campos: `full_name`, `email`, `is_active`
  
- **`BibtexImport`**: Controle de importações via BibTeX
  - Campos: `uploaded_by` (FK User), `bibtex_file`, `zip_file`, `total_entries`, `successful_imports`, `failed_imports`, `import_log`

### Sistema de Permissões

#### Níveis de Acesso
- **Superusuário/Staff**: Acesso completo ao Django Admin e funcionalidades administrativas
- **Usuários Autenticados**: Acesso às páginas públicas (mesmo que anônimos)
- **Usuários Anônimos**: Acesso completo às páginas públicas (busca, eventos, autores)

#### Proteção de Rotas
- Rotas administrativas protegidas com `@staff_member_required`
- Páginas públicas acessíveis sem autenticação
- Django Admin restrito a usuários staff

## Histórias Implementadas

### História 1: Gerenciamento de Eventos
**Como administrador, eu gostaria de cadastrar, editar e deletar eventos**

- **Views**: Admin interface para modelo `Event`
- **Funcionalidades**: CRUD completo (Create, Read, Update, Delete)
- **Validações**: Slug único baseado no acronym
- **Campos**: Nome, sigla, entidade promotora

### História 2: Gerenciamento de Edições de Eventos  
**Como administrador, eu quero cadastrar (editar, deletar) uma edição de evento**

- **Views**: Admin interface para modelo `Edition`
- **Funcionalidades**: CRUD completo com validações
- **Constraint**: Unicidade por evento/ano
- **Campos**: Evento (FK), ano, local

### História 3: Gerenciamento Manual de Artigos
**Como administrador, eu quero cadastrar (editar, deletar) um artigo manualmente, incluindo seu PDF**

- **Views**: Admin interface para modelo `Article`
- **Upload**: Suporte a PDFs organizados por evento/ano
- **Relacionamentos**: M:N com autores
- **Campos**: Título, autores, edição, páginas, PDF

### História 4: Importação em Massa via BibTeX
**Como administrador, eu quero cadastrar artigos em massa, a partir de um arquivo bibtex**

- **URL**: `/admin/bibtex-import/`
- **View**: `bibtex_import` com processamento customizado
- **Funcionalidades**: 
  - Upload de arquivo BibTeX + ZIP com PDFs
  - Validação de campos obrigatórios
  - Criação automática de eventos/edições
  - Relatório detalhado de importação
  - Notificações automáticas por email

### História 5: Busca de Artigos
**Como usuário, eu quero pesquisar por artigos: por título, por autor e por nome de evento**

- **URL**: `/search/`
- **View**: `search_articles`
- **Funcionalidades**:
  - Busca por título, autor ou evento
  - Resultados com links para detalhes
  - Interface simples com formulário GET

### História 6: Páginas Públicas de Eventos e Edições
**Como administrador, eu quero que todo evento tenha uma home page, com suas edições**

- **URLs**: `/<slug>/` (evento), `/<slug>/<year>/` (edição)
- **Views**: `event_detail`, `edition_detail`
- **Funcionalidades**:
  - Página do evento com lista de edições
  - Página da edição com lista de artigos
  - Navegação breadcrumb
  - Links para autores e PDFs

### História 7: Páginas de Autores
**Como usuário, eu quero ter uma home page com meus artigos, organizados por ano**

- **URL**: `/authors/<slug>/`
- **View**: `author_detail`
- **Funcionalidades**:
  - Lista de artigos organizados por ano
  - Ordenação cronológica decrescente
  - Links para artigos e eventos

### História 8: Sistema de Notificações
**Como usuário, eu quero me cadastrar para receber um mail sempre que eu tiver um novo artigo**

- **URL**: `/notifications/subscribe/`
- **View**: `notification_subscribe`
- **Funcionalidades**:
  - Cadastro por nome e email
  - Envio automático via signals do Django
  - Busca exata por nome do autor
  - Emails com dados completos do artigo

## Estrutura de URLs

### URLs Públicas
```python
/                              # Página inicial com estatísticas gerais
/search/                       # Sistema de busca de artigos
/events/                       # Lista de todos os eventos
/authors/                      # Lista de todos os autores
/notifications/subscribe/      # Cadastro para notificações
/articles/<int:pk>/           # Detalhes de um artigo específico
/<slug>/                      # Página do evento (ex: /sbes/)
/<slug>/<int:year>/           # Página da edição (ex: /sbes/2024/)
/authors/<slug>/              # Página do autor (ex: /authors/marco-tulio-valente/)
```

### URLs Administrativas
```python
/admin/                       # Django Admin principal
/login/                       # Login administrativo
/admin/logout/               # Logout administrativo
/bibtex-import/              # Interface de importação BibTeX
/admin/bibtex-import/        # Redirecionamento para admin de importações
```

### Padrões de URL
- **Slugs**: URLs amigáveis baseadas em slugs (sbes, marco-tulio-valente)
- **Hierarquia**: Evento → Edição → Artigo
- **REST-like**: Recursos identificáveis por URLs únicas

## Funcionalidades Técnicas

### Sistema de Upload e Organização de PDFs
- **Estrutura**: `media/articles/<evento-slug>/<ano>/<arquivo>.pdf`
- **Upload Individual**: Via Django Admin com interface de arquivo
- **Upload em Massa**: Via ZIP na importação BibTeX
- **Validação**: Verificação de formato e tamanho de arquivo

### Sistema de Busca Avançado
- **Tipos de Busca**: Título, autor, nome do evento
- **Algoritmo**: Busca case-insensitive com `icontains`
- **Performance**: Queries otimizadas com `select_related` e `prefetch_related`
- **Interface**: Formulário simples com dropdown de tipo de busca

### Importação BibTeX Robusta
- **Validação Rigorosa**: Campos obrigatórios (title, author, booktitle, year)
- **Auto-criação**: Eventos e edições criados automaticamente se não existirem
- **Processamento de Autores**: Suporte a múltiplos autores com parsing inteligente
- **Relatório Detalhado**: Log completo de sucessos, falhas e motivos
- **Integração com PDFs**: Matching automático de PDFs do ZIP via chave BibTeX

### Sistema de Notificações Inteligente
- **Trigger**: Django signals (`m2m_changed`) para detectar novos artigos
- **Matching**: Busca exata case-insensitive por nome do autor
- **Email**: Templates HTML com dados completos do artigo
- **Performance**: Processamento assíncrono para não bloquear interface

### Interface Administrativa Avançada
- **Django Admin Customizado**: Filtros, buscas e autocomplete
- **Hierarquia Visual**: Inline editing de edições e artigos
- **Contadores**: Estatísticas em tempo real
- **Bulk Actions**: Ações em massa para múltiplos registros

### Tecnologias e Stack

### Backend
- **Django 5.2.5**: Framework web principal
- **Python 3.11**: Linguagem de programação
- **SQLite**: Banco de dados (desenvolvimento)
- **bibtexparser 1.4.1**: Parsing de arquivos BibTeX
- **Django Admin**: Interface administrativa

### Frontend
- **Bootstrap 5**: Framework CSS responsivo
- **HTML/CSS/JavaScript**: Tecnologias web padrão
- **Django Templates**: Sistema de templates nativo
- **Icons**: Bootstrap Icons para interface

### Infraestrutura
- **Conda**: Gerenciamento de ambiente e dependências
- **Git**: Controle de versão
- **Email Backend**: Configurável (console/SMTP)

## Guia de Uso

### 1. Configuração Inicial

#### Usando Conda (Recomendado)
```bash
# Clonar repositório
git clone https://github.com/HaniBR01/paperpaper.git
cd paperpaper

# Criar ambiente conda
conda env create -f environment.yml

# Ativar ambiente
conda activate paperpaper

# Configurar banco de dados
python manage.py migrate

# Criar superusuário
python manage.py createsuperuser

# Iniciar servidor
python manage.py runserver
```



### 2. Configuração de Permissões
```bash
# Executar script de permissões (se necessário)
python manage.py shell < setup_permissions.py
```

### 3. Acesso ao Sistema
- **Página Principal**: http://localhost:8000/
- **Admin Django**: http://localhost:8000/admin/
- **Importação BibTeX**: http://localhost:8000/bibtex-import/

### 4. Fluxo de Trabalho Típico

#### Para Administradores:
1. Acesse o Django Admin
2. Crie eventos (SBES, SBCARS, etc.)
3. Crie edições dos eventos (SBES 2024, etc.)
4. Cadastre artigos:
   - **Manualmente**: Via admin Django
   - **Em Massa**: Via importação BibTeX

#### Para Usuários:
1. Use a busca para encontrar artigos
2. Navegue pelas páginas de eventos e edições
3. Acesse páginas de autores
4. Cadastre-se para receber notificações

### Dependências do Projeto

O projeto utiliza **Conda** para gerenciamento de ambiente e dependências através do arquivo `environment.yml`:

```yaml
name: paperpaper
channels:
  - conda-forge
  - defaults
dependencies:
  - python=3.11
  - django=5.2.5
  - sqlite
  - pip
  - pip:
    - asgiref==3.9.1
    - sqlparse==0.5.3
    - tzdata==2025.2
    - bibtexparser==1.4.1
```

### 5. Importação BibTeX - Exemplo

```bibtex
@inproceedings{exemplo2024,
    author = {João Silva and Maria Santos},
    title = {Uma Abordagem Inovadora para Engenharia de Software},
    booktitle = {Anais do XXXVIII Simpósio Brasileiro de Engenharia de Software},
    year = {2024},
    pages = {1--10},
    location = {Curitiba/PR}
}
```

1. Prepare arquivo `.bib` com entradas válidas
2. (Opcional) Prepare ZIP com PDFs nomeados pela chave BibTeX
3. Acesse `/bibtex-import/`
4. Faça upload dos arquivos
5. Aguarde processamento e verifique relatório

## Estrutura de Diretórios

```
paperpaper/
├── 📁 docs/                          # Documentação
│   ├── historia_1.md                 # Backlog História 1
│   ├── historia_2.md                 # Backlog História 2
│   ├── historia_3.md                 # Backlog História 3
|   ├── historia_4.md                 # Backlog História 4
│   ├── historia_5.md                 # Backlog História 5
│   ├── historia_6.md                 # Backlog História 6
│   ├── historia_7.md                 # Backlog História 7
|   ├── historia_8.md                 # Backlog História 8
│   ├── IMPLEMENTACAO.md              # Este arquivo
│   ├── testes_de_aceitacao.txt       # Especificação dos testes
│   ├── sequence-diagram.md           # Diagrama de sequência
│   └── package-diagram.md            # Diagrama de pacotes
├── 📁 media/                         # Arquivos de mídia
│   ├── articles/                     # PDFs dos artigos
│   │   ├── sbes/2024/               # Organizados por evento/ano
│   │   └── sbcars/2023/
│   └── imports/                      # Arquivos de importação
│       ├── bibtex/                   # Arquivos BibTeX
│       └── pdfs/                     # ZIPs temporários
├── 📁 paperpaper/                    # App principal Django
│   ├── __init__.py
│   ├── admin.py                      # Configuração do Django Admin
│   ├── asgi.py                      # Configuração ASGI
│   ├── models.py                     # Modelos de dados
│   ├── settings.py                   # Configurações Django
│   ├── urls.py                      # Roteamento de URLs
│   ├── views.py                     # Views/Controllers
│   ├── wsgi.py                      # Configuração WSGI
│   ├── migrations/                   # Migrações do banco
│   └── templates/paperpaper/         # Templates HTML
│       ├── base.html                # Template base
│       ├── home.html                # Página inicial
│       ├── search.html              # Sistema de busca
│       ├── event_detail.html        # Página do evento
│       ├── edition_detail.html      # Página da edição
│       ├── author_detail.html       # Página do autor
│       ├── bibtex_import.html       # Importação BibTeX
│       └── notification_subscribe.html # Notificações
├── 📄 manage.py                     # Django management
├── 📄 db.sqlite3                    # Banco de dados SQLite
├── 📄 environment.yml               # Dependências Conda
├── 📄 setup_permissions.py          # Script de permissões
```

## Performance e Otimizações

### Otimizações de Banco de Dados
- **Select Related**: Redução de queries para ForeignKeys
- **Prefetch Related**: Otimização de relacionamentos M:N
- **Database Indexes**: Campos frequentemente pesquisados
- **Unique Constraints**: Garantia de integridade dos dados

### Otimizações de Interface
- **Bootstrap CDN**: Carregamento rápido de estilos
- **Lazy Loading**: Imagens carregadas sob demanda
- **Paginação**: Implementável para listas grandes
- **Caching**: Preparado para cache de queries frequentes

### Tratamento de Erros
- **404 Handlers**: Páginas personalizadas para recursos não encontrados
- **Form Validation**: Validação client-side e server-side
- **File Upload**: Validação de tipos e tamanhos de arquivo
- **Error Logging**: Sistema de logs configurável

## Considerações de Produção

### Segurança
- **CSRF Protection**: Habilitado por padrão no Django
- **SQL Injection**: Prevenido pelo Django ORM
- **XSS Protection**: Templates com escape automático
- **File Upload**: Validação de tipos de arquivo
- **Admin Access**: Restrito a usuários staff

### Configurações Recomendadas para Produção

#### settings.py
```python
DEBUG = False
ALLOWED_HOSTS = ['seu-dominio.com']

# Configuração de email real
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'seu-email@gmail.com'
EMAIL_HOST_PASSWORD = 'sua-senha-app'

# Configuração de banco para produção
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'paperpaper_prod',
        'USER': 'paperpaper_user',
        'PASSWORD': 'senha_segura',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Configuração de arquivos estáticos
STATIC_ROOT = '/var/www/paperpaper/static/'
MEDIA_ROOT = '/var/www/paperpaper/media/'
```

#### Servidor Web
```nginx
# nginx.conf
server {
    listen 80;
    server_name seu-dominio.com;
    
    location /static/ {
        alias /var/www/paperpaper/static/;
    }
    
    location /media/ {
        alias /var/www/paperpaper/media/;
    }
    
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

