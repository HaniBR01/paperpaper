# Diagrama de Sequência - Importação BibTeX

Este diagrama mostra o fluxo de execução da importação de artigos via BibTeX, uma das funcionalidades mais importantes do sistema PaperPaper.

```mermaid
sequenceDiagram
    participant U as Administrador
    participant V as BibtexImportView
    participant M as Models
    participant P as BibtexParser
    participant DB as Database
    participant E as EmailService

    Note over U,E: Processo de Importação BibTeX + ZIP

    U->>V: POST /admin/bibtex-import/
    Note right of U: Upload BibTeX + ZIP

    V->>V: validate_files()
    alt Arquivo BibTeX ausente
        V->>U: Error: "Arquivo BibTeX obrigatório"
    end

    V->>M: BibtexImport.objects.create()
    M->>DB: INSERT bibtex_import
    DB-->>M: import_record

    V->>P: bibtexparser.loads(bibtex_content)
    P-->>V: bib_database

    V->>V: extract_pdfs_from_zip()
    Note right of V: Extrair PDFs do ZIP

    loop Para cada entrada BibTeX
        V->>V: process_bibtex_entry()
        
        V->>M: Event.objects.get_or_create()
        M->>DB: SELECT/INSERT event
        DB-->>M: event
        
        V->>M: Edition.objects.get_or_create()
        M->>DB: SELECT/INSERT edition
        DB-->>M: edition
        
        V->>M: Author.objects.get_or_create()
        M->>DB: SELECT/INSERT authors
        DB-->>M: authors[]
        
        V->>M: Article.objects.create()
        M->>DB: INSERT article
        DB-->>M: article
        
        V->>M: article.authors.set(authors)
        M->>DB: INSERT article_authors
        
        alt PDF disponível
            V->>M: article.pdf_file.save()
            M->>DB: UPDATE article + save file
        end
        
        V->>E: send_notifications_for_article()
        loop Para cada autor cadastrado
            E->>M: NotificationSubscription.objects.filter()
            M->>DB: SELECT subscriptions
            DB-->>M: subscriptions[]
            E->>E: send_mail()
        end
    end

    V->>M: import_record.update_stats()
    M->>DB: UPDATE import_record

    V->>U: Success/Warning message
    Note right of V: Relatório de importação

    U->>V: GET /admin/paperpaper/bibteximport/
    V->>U: Lista de importações com estatísticas
```

## Fluxo Detalhado

### 1. **Validação Inicial**
- Upload de arquivo BibTeX (obrigatório)
- Upload de ZIP com PDFs (opcional)
- Validação de tipos de arquivo

### 2. **Processamento BibTeX**
- Parse do arquivo BibTeX
- Extração de metadados (título, autor, evento, ano)
- Validação de campos obrigatórios

### 3. **Criação de Entidades**
- **Eventos**: Criados baseado no campo `booktitle`
- **Edições**: Associadas ao evento + ano
- **Autores**: Parseados do campo `author`
- **Artigos**: Criados com todos os metadados

### 4. **Processamento de Arquivos**
- Associação de PDFs baseada na chave BibTeX
- Upload para `media/articles/{evento}/{ano}/`

### 5. **Notificações**
- Envio automático para autores cadastrados
- Sistema de inscrições por email

### 6. **Relatório Final**
- Estatísticas de sucesso/falha
- Log detalhado de processamento
- Interface administrativa para acompanhamento