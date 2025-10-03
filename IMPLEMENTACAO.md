# PaperPaper - Sistema de Gerenciamento de Artigos Acadêmicos

## Resumo da Implementação

O sistema PaperPaper foi implementado como um projeto Django único, organizando todas as funcionalidades no app principal. A arquitetura segue os requisitos dos testes de aceitação, oferecendo uma divisão clara entre usuários administradores e usuários comuns.

## Estrutura Implementada

### Modelos de Dados
- **Event**: Eventos acadêmicos (SBES, SBCARS, etc.)
- **Edition**: Edições específicas dos eventos (SBES 2024, etc.)
- **Article**: Artigos acadêmicos com autores, páginas e PDFs
- **Author**: Autores dos artigos
- **NotificationSubscription**: Inscrições para notificações por email
- **BibtexImport**: Controle de importações via BibTeX

### Sistema de Usuários e Permissões
- **Superusuário/Staff**: Acesso total ao Django Admin
- **Grupo Administradores**: CRUD completo de todos os modelos
- **Grupo Usuários**: Apenas visualização de conteúdo público
- **Usuários anônimos**: Acesso às páginas públicas

### Funcionalidades por Tipo de Usuário

#### ADMINISTRADORES (Testes 1-4)
✅ **Teste 1**: Cadastrar/editar/deletar eventos via Django Admin
✅ **Teste 2**: Cadastrar/editar/deletar edições via Django Admin  
✅ **Teste 3**: Cadastrar artigos manualmente via Django Admin (com upload de PDF)
✅ **Teste 4**: Importar artigos em massa via BibTeX + ZIP (interface customizada)

#### USUÁRIOS (Testes 5-8)
✅ **Teste 5**: Sistema de busca por título, autor e evento (`/search/`)
✅ **Teste 6**: Páginas públicas de eventos e edições (`/sbes/`, `/sbes/2024/`)
✅ **Teste 7**: Páginas de autores organizadas por ano (`/authors/marco-tulio-valente/`)
✅ **Teste 8**: Sistema de notificações por email (`/notifications/subscribe/`)

## URLs Implementadas

```
/                           - Página inicial com estatísticas
/search/                    - Sistema de busca
/notifications/subscribe/   - Cadastro para notificações
/admin/                     - Django Admin (staff only)
/admin/bibtex-import/      - Importação BibTeX (staff only)
/<sigla>/                  - Página do evento (ex: /sbes/)
/<sigla>/<ano>/            - Página da edição (ex: /sbes/2024/)
/authors/<slug>/           - Página do autor
```

## Características Técnicas

### Upload e Organização de PDFs
- PDFs organizados por evento/ano: `media/articles/sbes/2024/`
- Upload individual via admin ou em massa via ZIP

### Sistema de Busca
- Busca por título, autor ou evento
- Resultados com links para páginas específicas
- Interface simples e intuitiva

### Importação BibTeX
- Validação de campos obrigatórios (title, author, booktitle, year)
- Criação automática de eventos/edições se não existirem
- Processamento de autores múltiplos
- Relatório detalhado de sucessos/falhas
- Notificações automáticas por email

### Sistema de Notificações
- Cadastro por nome e email
- Envio automático quando artigos são adicionados
- Busca exata por nome do autor

### Interface Administrativa
- Django Admin customizado com filtros e buscas
- Visualização hierárquica (eventos → edições → artigos)
- Contadores e estatísticas
- Interface para importação BibTeX

## Como Usar

### 1. Iniciar o Sistema
```bash
docker-compose up
```

### 2. Acessar o Sistema
- **Página inicial**: http://localhost:8000/
- **Admin**: http://localhost:8000/admin/ (usuário: admin)

### 3. Configurar Permissões
```bash
docker-compose run --rm web python manage.py shell < setup_permissions.py
```

### 4. Cadastrar Dados
1. Acesse o admin Django
2. Crie eventos (SBES, SBCARS)
3. Crie edições (SBES 2024, etc.)
4. Cadastre artigos manualmente ou use importação BibTeX

### 5. Testar Funcionalidades
- Use a busca para encontrar artigos
- Navegue pelas páginas públicas
- Cadastre-se para notificações
- Teste a importação BibTeX com o arquivo fornecido

## Estrutura de Arquivos

```
paperpaper/
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── manage.py
├── setup_permissions.py
├── paperpaper/
│   ├── settings.py
│   ├── urls.py
│   ├── models.py
│   ├── admin.py
│   ├── views.py
│   └── migrations/
└── templates/paperpaper/
    ├── base.html
    ├── home.html
    ├── search.html
    ├── event_detail.html
    ├── edition_detail.html
    ├── author_detail.html
    ├── notification_subscribe.html
    └── bibtex_import.html
```

## Próximos Passos

O sistema está completo e atende todos os testes de aceitação. Para produção, recomenda-se:

1. Configurar email real (SMTP)
2. Adicionar paginação nas listas
3. Implementar sistema de cache
4. Configurar servidor web (nginx + gunicorn)
5. Configurar backup do banco de dados
6. Adicionar logs e monitoramento
