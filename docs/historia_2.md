# História #2: Como administrador, eu quero cadastrar (editar, deletar) uma edição de evento

## Descrição do Teste de Aceitação

- Cadastrar a edição de 2024 do SBES. Dados: ano da edição e local (no caso, Curitiba).

- Editar os dados de uma edição existente.

- Deletar uma edição.

- Funcionalidades CRUD completas: Create, Read, Update, Delete.

## Tarefas e Responsáveis

### Modelagem e Admin
1. Criar/Refinar o Modelo Edition: Garantir que o modelo em paperpaper/models.py tenha os campos event (ForeignKey), year, location e timestamps com validações adequadas.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

2. Configurar o Admin: Adicionar Edition ao paperpaper/admin.py para permitir CRUD via interface administrativa com filtros, busca e autocomplete.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Backend/Views
3. Implementar validações de negócio: Garantir unicidade de edição por evento/ano e integridade referencial.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

4. Otimizar consultas: Usar select_related e prefetch_related para performance nas consultas de edições com eventos e artigos.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Database/Migrations
5. Criar migrações: Implementar as migrações necessárias para o modelo Edition com constraints de unicidade.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Testes de Aceitação
6. Testar CRUD Completo: Executar o teste de aceitação - criar edição SBES 2024 em Curitiba, editar localização, verificar listagem e testar exclusão.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

### Validações e Segurança
7. Implementar validações de dados: Validar ano (range válido), local (não vazio) e relacionamento com evento existente.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]

8. Configurar permissões: Garantir que apenas administradores possam realizar operações CRUD em edições.

    [Haniel + Copilot - Agentic (Claude Sonnet 3.5)]
