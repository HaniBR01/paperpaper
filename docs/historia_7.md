# História #7: Como usuário, eu quero ter uma home page com meus artigos, organizados por ano

## Descrição do Teste de Aceitação

- Acessar a página de um autor cadastrado (ex: Marco Tulio Valente) através de uma URL baseada em seu ID (ex: `/authors/1/`).
- Verificar se a página lista corretamente todos os artigos do autor.
- Confirmar que a listagem de artigos está ordenada por ano, do mais recente para o mais antigo.
- Assegurar que todos os artigos do autor são exibidos na mesma página, sem paginação.

## Tarefas e Responsáveis

### Modelagem e Admin  
1. Verificar o Modelo `Author`: Confirmar que o modelo `Author` em `paperpaper/models.py` possui a chave primária (ID) padrão do Django.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

2. Configurar o Admin: Garantir que o modelo `Author` está registrado em `paperpaper/admin.py` para facilitar a consulta de IDs.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### Backend/Views  
3. Implementar View `author_detail`: Criar a view em `paperpaper/views.py` que busca um autor pela sua `pk` (chave primária) e retorna seus artigos ordenados por ano.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### URLs  
4. Configurar a Rota: Adicionar a URL `authors/<int:pk>/` em `paperpaper/urls.py`.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### Frontend/Templates  
5. Criar `author_detail.html`: Implementar o template que exibe as informações do autor e a lista de seus artigos.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

6. Atualizar Links nos Templates: Em todas as páginas que listam autores, transformar seus nomes em links que apontem para a nova página de detalhes, usando o ID do autor (`author.pk`).

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### Testes de Aceitação  
7. Executar Teste Manual: Realizar o teste de aceitação: navegar para a página de um autor (usando seu ID, ex: `/authors/1/`) e verificar se a exibição e a ordenação dos artigos estão corretas.

    [Heitor]