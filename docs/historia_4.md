# História #4: Como administrador, eu quero cadastrar artigos em massa via arquivo BibTeX

## Descrição do Teste de Aceitação

Como administrador, eu quero cadastrar artigos em massa via arquivo BibTeX, permitindo:

- Upload de arquivo BibTeX contendo múltiplos artigos
- Upload opcional de arquivo ZIP com PDFs correspondentes
- Validação de campos obrigatórios
- Relatório detalhado de importação

## Tarefas e Responsáveis

### Backend / Views
1. Implementar view `bibtex_import` em `paperpaper/views.py`:
   - Processamento do upload de arquivos (BibTeX + ZIP opcional)
   - Validação de formatos e conteúdo
   - Geração de relatório detalhado
   - Feedback via mensagens do Django

   [João Pedro + Copilot]

2. Implementar processamento BibTeX:
   - Parse do arquivo usando bibtexparser
   - Validação de campos obrigatórios (title, author, booktitle, year)
   - Extração e validação de PDFs do ZIP
   - Associação BibTeX key com PDFs

   [João Pedro + Copilot]

3. Criar testes unitários:
   - Upload de BibTeX válido
   - Upload com ZIP de PDFs
   - Campos obrigatórios faltando
   - Anos inválidos
   - PDFs não correspondentes

   [João Pedro]

### Models
4. Criar modelo `BibtexImport`:
   - Campos para arquivos (BibTeX e ZIP)
   - Campos para estatísticas
   - Campo para log detalhado
   - Relacionamento com usuário

   [João Pedro + Copilot]

### Templates / Frontend
5. Criar template `bibtex_import.html`:
   - Formulário de upload com dois campos
   - Exemplos e instruções claras
   - Alertas para campos obrigatórios
   - Relatório visual de importação

   [João Pedro + Copilot]

6. Configurar interface administrativa:
   - Lista de importações com filtros
   - Visualização de detalhes/log
   - Ações em massa se necessário
   - Links para artigos importados

   [João Pedro + Copilot]

### Segurança e Validação
7. Implementar validação de arquivos:
   - Tamanho máximo de uploads
   - Tipos MIME permitidos
   - Sanitização de nomes

   [João Pedro + Copilot]

8. Configurar CSRF e permissões:
   - Acesso restrito a staff
   - Validação de permissões
   - Log de ações

   [João Pedro + Copilot]

### UX / Feedback
9. Adicionar feedback em tempo real:
   - Barra de progresso
   - Contadores de sucesso/falha
   - Alertas formatados
   - Links para itens criados

   [João Pedro + Copilot]