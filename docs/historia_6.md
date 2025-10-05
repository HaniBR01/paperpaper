# História #6: Como administrador, eu quero que todo evento tenha uma home page, com suas edições; cada edição, por sua vez, também deve ter uma home page, com seus artigos

## Descrição do Teste de Aceitação

- Acessar a página `/sbes` que deve mostrar as edições do SBES cadastradas (no caso, apenas a de 2024). 
- Ao clicar na edição 2024, ir para a página `/sbes/2024` que deve mostrar todos os artigos desta edição.
- Verificar se cada artigo exibe seus dados completos (título, autores, páginas, PDF quando disponível).
- Confirmar que os links para autores funcionam corretamente.
- Validar que a navegação breadcrumb está funcionando.

## Tarefas e Responsáveis

### Backend/Views
1. **Implementar view `event_detail`**: Criar view em `paperpaper/views.py` que recebe slug do evento e exibe suas edições disponíveis ordenadas por ano descendente.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

2. **Implementar view `edition_detail`**: Criar view que recebe slug do evento + ano e exibe todos os artigos da edição específica com otimização de consultas.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

3. **Otimizar consultas de banco**: Usar `select_related` e `prefetch_related` para evitar N+1 queries ao carregar eventos, edições e artigos com relacionamentos.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### URLs/Routing
4. **Configurar rotas em `paperpaper/urls.py`**: Adicionar URL patterns `<slug:slug>/` para eventos e `<slug:slug>/<int:year>/` para edições, garantindo ordem correta.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

5. **Resolver conflitos de URL**: Posicionar rotas específicas (`events/`, `authors/`, `search/`) antes das rotas genéricas com slug para evitar captura incorreta.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Frontend/Templates
6. **Criar `event_detail.html`**: Implementar template que exibe informações do evento e lista suas edições em cards Bootstrap com ano, local e contagem de artigos.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

7. **Criar `edition_detail.html`**: Implementar template que exibe artigos da edição em list-group, com links para autores e botões de download de PDF.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

8. **Implementar navegação breadcrumb**: Adicionar breadcrumbs em ambos templates (Início > Evento > Edição) para melhor navegação.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Modelagem e Integrações
9. **Implementar `get_absolute_url` nos models**: Adicionar métodos nos models `Event` e `Edition` para facilitar geração de URLs nos templates e admin.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

10. **Validar integridade de slugs**: Garantir que os slugs dos eventos são únicos e seguem padrão baseado no acronym, com tratamento de caracteres especiais.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Validações e Tratamento de Erros
12. **Implementar tratamento de 404**: Garantir que URLs inválidas (evento/edição inexistente) retornem página 404 apropriada usando `get_object_or_404`.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

13. **Validar dados de entrada**: Verificar formato do ano nas URLs e existência de relacionamentos entre evento e edição.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Testes de Aceitação
14. **Executar teste completo**: Testar as URLs `/sbes` e `/sbes/2024` conforme especificado, verificando exibição correta de dados e funcionalidade de links.

    [Haniel]

## Status Atual

A **História 6** refere-se à implementação de páginas públicas para eventos e suas edições, permitindo navegação hierárquica do tipo `/evento` → `/evento/ano`.

## Observações Técnicas

- **Padrão de URLs**: Seguir estrutura `/evento-slug/` e `/evento-slug/ano/`
- **Otimização**: Minimizar queries com `select_related`/`prefetch_related`
- **Responsividade**: Usar Bootstrap para interface consistente
- **SEO**: Considerar meta tags específicas para cada página