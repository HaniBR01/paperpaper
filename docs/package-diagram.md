# Diagrama de Pacotes - Arquitetura do Sistema

Este diagrama mostra a organização arquitetural do sistema PaperPaper seguindo o padrão MVT (Model-View-Template) do Django.

```mermaid
graph TB
    subgraph "🌐 Presentation Layer"
        subgraph "📱 Web Interface"
            TEMPLATES["`**Templates**
            • base.html
            • home.html
            • event_detail.html
            • edition_detail.html
            • author_detail.html
            • search.html
            • bibtex_import.html
            • notification_subscribe.html`"]
            
            STATIC["`**Static Files**
            • Bootstrap 5 CSS
            • JavaScript
            • Icons (Bootstrap Icons)
            • Custom Styles`"]
        end
        
        subgraph "🔧 Admin Interface"
            ADMIN_TEMPLATES["`**Admin Templates**
            • app_index.html
            • Custom admin forms
            • BibTeX import interface`"]
        end
    end

    subgraph "⚡ Application Layer"
        subgraph "🎯 Views Package"
            PUBLIC_VIEWS["`**Public Views**
            • home()
            • event_detail()
            • edition_detail()
            • author_detail()
            • search_articles()
            • notification_subscribe()`"]
            
            ADMIN_VIEWS["`**Admin Views**
            • bibtex_import()
            • handle_bibtex_upload()
            • process_bibtex_entry()`"]
        end
        
        subgraph "🛣️ URL Routing"
            URLS["`**URL Configuration**
            • / → home
            • /admin/ → admin
            • /<slug>/ → event_detail
            • /<slug>/<year>/ → edition_detail
            • /authors/<slug>/ → author_detail
            • /admin/bibtex-import/ → bibtex_import`"]
        end
        
        subgraph "🔐 Authentication & Authorization"
            AUTH["`**Django Auth**
            • User Management
            • Groups & Permissions
            • @staff_member_required
            • Admin Access Control`"]
        end
    end

    subgraph "💾 Data Layer"
        subgraph "📋 Models Package"
            CORE_MODELS["`**Core Models**
            • Event
            • Edition
            • Article
            • Author`"]
            
            SYSTEM_MODELS["`**System Models**
            • NotificationSubscription
            • BibtexImport
            • User (Django built-in)`"]
        end
        
        subgraph "🗄️ Database"
            DATABASE["`**SQLite Database**
            • Events Table
            • Editions Table
            • Articles Table
            • Authors Table
            • Article_Authors (M2M)
            • Notifications Table
            • BibTeX Imports Table`"]
        end
        
        subgraph "📁 File Storage"
            MEDIA["`**Media Files**
            • articles/{event}/{year}/*.pdf
            • imports/bibtex/*.txt
            • imports/pdfs/*.zip`"]
        end
    end

    subgraph "🔧 Infrastructure Layer"
        subgraph "⚙️ Django Framework"
            DJANGO_CORE["`**Django Core**
            • ORM
            • Admin Interface
            • Authentication
            • URL Routing
            • Template Engine
            • Static Files Handler`"]
        end
        
        subgraph "📦 External Libraries"
            LIBRARIES["`**Third-party**
            • bibtexparser
            • Bootstrap 5
            • zipfile (Python)
            • email (Django)`"]
        end
        
        subgraph "⚡ Services"
            EMAIL_SERVICE["`**Email Service**
            • SMTP Configuration
            • Notification System
            • Author Alerts`"]
        end
    end

    %% Relationships
    TEMPLATES --> PUBLIC_VIEWS
    TEMPLATES --> ADMIN_VIEWS
    ADMIN_TEMPLATES --> ADMIN_VIEWS
    
    PUBLIC_VIEWS --> CORE_MODELS
    ADMIN_VIEWS --> CORE_MODELS
    ADMIN_VIEWS --> SYSTEM_MODELS
    
    CORE_MODELS --> DATABASE
    SYSTEM_MODELS --> DATABASE
    
    ADMIN_VIEWS --> MEDIA
    ADMIN_VIEWS --> EMAIL_SERVICE
    
    URLS --> PUBLIC_VIEWS
    URLS --> ADMIN_VIEWS
    
    AUTH --> ADMIN_VIEWS
    AUTH --> DJANGO_CORE
    
    PUBLIC_VIEWS --> DJANGO_CORE
    ADMIN_VIEWS --> DJANGO_CORE
    CORE_MODELS --> DJANGO_CORE
    
    ADMIN_VIEWS --> LIBRARIES
    EMAIL_SERVICE --> LIBRARIES

    %% Styling
    classDef presentationColor fill:#e1f5fe,stroke:#01579b,stroke-width:2px
    classDef applicationColor fill:#f3e5f5,stroke:#4a148c,stroke-width:2px
    classDef dataColor fill:#e8f5e8,stroke:#1b5e20,stroke-width:2px
    classDef infrastructureColor fill:#fff3e0,stroke:#e65100,stroke-width:2px
    
    class TEMPLATES,STATIC,ADMIN_TEMPLATES presentationColor
    class PUBLIC_VIEWS,ADMIN_VIEWS,URLS,AUTH applicationColor
    class CORE_MODELS,SYSTEM_MODELS,DATABASE,MEDIA dataColor
    class DJANGO_CORE,LIBRARIES,EMAIL_SERVICE infrastructureColor
```

## Descrição da Arquitetura

### 🌐 **Presentation Layer (Camada de Apresentação)**
- **Templates**: Interface do usuário usando Django Templates + Bootstrap
- **Static Files**: Recursos estáticos (CSS, JS, imagens)
- **Admin Interface**: Interface administrativa customizada do Django

### ⚡ **Application Layer (Camada de Aplicação)**
- **Views**: Lógica de negócio e controle de fluxo
- **URL Routing**: Mapeamento de URLs para views
- **Authentication**: Sistema de autenticação e autorização

### 💾 **Data Layer (Camada de Dados)**
- **Models**: Modelos de dados usando Django ORM
- **Database**: Banco de dados SQLite para persistência
- **File Storage**: Armazenamento de arquivos PDF e uploads

### 🔧 **Infrastructure Layer (Camada de Infraestrutura)**
- **Django Framework**: Framework web principal
- **External Libraries**: Bibliotecas de terceiros
- **Services**: Serviços externos (email, etc.)

## Principais Características

### 📊 **Separação de Responsabilidades**
- Cada camada tem responsabilidades bem definidas
- Baixo acoplamento entre componentes
- Alta coesão dentro de cada pacote

### 🔄 **Fluxo de Dados**
1. **Request** → URLs → Views
2. **Views** → Models → Database
3. **Views** → Templates → **Response**

### 🛡️ **Segurança**
- Autenticação baseada em sessões
- Autorização por grupos e permissões
- Proteção CSRF automática do Django

### 📈 **Escalabilidade**
- Arquitetura modular facilita expansão
- ORM permite migração para outros SGBDs
- Sistema de templates reutilizáveis