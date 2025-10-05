# História #3: Como administrador, eu quero cadastrar (editar, deletar) um artigo manualmente, incluindo seu pdf

## Descrição do Teste de Aceitação

- Cadastrar três artigos do SBES 2024, usando os dados e PDFs obtidos das seguintes URLs:
  - `https://sol.sbc.org.br/index.php/sbes/article/view/30356`
  - `https://sol.sbc.org.br/index.php/sbes/article/view/30367`
  - `https://sol.sbc.org.br/index.php/sbes/article/view/30374`
- Editar os dados de um dos artigos recém-cadastrados (ex: o título).
- Deletar um dos artigos recém-cadastrados.

## Tarefas e Responsáveis

### Modelagem e Admin  
1. Refinar o Modelo `Article`: Adicionar o campo `FileField` para o PDF em `paperpaper/models.py` e executar a migração.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

2. Configurar o Admin: Registrar o modelo `Article` em `paperpaper/admin.py` para permitir o gerenciamento via interface de administração.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### Backend/Views  
3. Implementar `ArticleForm`: Criar um `ModelForm` em um novo arquivo `paperpaper/forms.py` para o modelo `Article`.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

4. Implementar View `article_create`: Criar a view para o formulário de adição de novos artigos.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

5. Implementar View `article_edit`: Criar a view para carregar e atualizar artigos existentes.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

6. Implementar View `article_delete`: Criar a view de confirmação e a lógica para a remoção de artigos.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### URLs  
7. Configurar as Rotas: Adicionar as URLs para `create`, `edit` e `delete` de artigos em `paperpaper/urls.py`.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### Frontend/Templates  
8. Criar `article_form.html`: Implementar o template de formulário reutilizável para criação e edição.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

9. Criar `article_confirm_delete.html`: Implementar o template de confirmação de exclusão.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

10. Integrar Botões de Ação: Adicionar os botões "Novo Artigo", "Editar" e "Deletar" nas interfaces apropriadas, visíveis apenas para administradores.

    [Heitor + Copilot - Agentic (Claude Sonnet 3.5)]

### Testes de Aceitação  
11. Executar Teste Manual: Realizar os testes de aceitação: cadastrar os 3 artigos, editar um e deletar outro, verificando o resultado a cada passo.

    [Heitor]