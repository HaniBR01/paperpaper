# História #5: Como usuário, eu quero pesquisar por artigos: por título, por autor e por nome de evento


## Descrição do Teste de Aceitação

- Informar uma substring e o campo no qual se deseja pesquisá-la (título, autor ou nome do evento).

- Deve ser mostrado uma “lista de resposta”, com todos os dados de todos os artigos que atenderam à pesquisa.
- As respostas podem ser mostradas de forma “contínua”, em uma mesma página.

## Tarefas e Responsáveis

### Backend / Views
1. Implementar view `search_articles` em `paperpaper/views.py`: Recebe GET com parâmetros `q` (termo) e `type` (title, author, event); realiza busca sobre os modelos Article, Author e Event; retorna contexto com lista de artigos encontrados e o termo/seleção da busca.  

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

2. Otimizar consultas: Usar `select_related`/`prefetch_related` para evitar N+1 ao buscar autores e eventos; indexar campos frequentemente pesquisados (ex.: title, author name, event name) se necessário.  

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

3. Testes unitários da view: Cobrir buscas por cada tipo, busca sem resultados e comportamento com caracteres especiais.  

    [Giovanni]

### URLs
4. Adicionar rota em `paperpaper/urls.py`:
   - `path('search/', views.search_articles, name='search_articles')`

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

### Templates / Frontend
5. Criar `paperpaper/templates/paperpaper/search.html`:  
   - Formulário com select para o tipo (Título / Autor / Evento) e input de texto com método GET.  
   - Exibição da lista de resultados com:
     - **Título** do artigo (link para detalhe do artigo);
     - **Autores** (cada autor com link para sua página);
     - **Evento** (link para página do evento);
     - **Resumo** e metadados relevantes (ano, DOI, páginas);
     - Botão/link de download do PDF quando disponível;
     - Mensagem clara quando nenhum resultado for encontrado.  
   - Uso de Bootstrap para responsividade e ícones `bi-*` para ações (search, file-earmark-pdf, person, building).
 
   [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

6. Reutilizar blocos do `base.html` e componentes (alerts para mensagens de sucesso/erro; list group/cards para resultados).  

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

### Segurança e Validação
7. Validação do parâmetro `type`: aceitar apenas os valores permitidos; sanitizar o termo `q` e evitar interpolação direta em consultas.  
   
    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

8. CSRF: Formulário de busca usa método GET e não precisa de token, garantir que quaisquer ações posteriores (download protegido, etc.) têm proteção adequada.  

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

### UX / Feedback
9. Adicionar feedback visual:
   - Alert ou badge com número de resultados.
   - Indicação de critérios usados na busca (por exemplo, "Busca por título: 'deep learning'").  

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]
