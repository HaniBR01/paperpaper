# História #1: Como administrador, eu gostaria de cadastrar, editar e deletar eventos

## Descrição do Teste de Aceitação

- Criar o evento: Simpósio Brasileiro de Engenharia de Software (SBES). Dados: Nome, Sigla (SBES), Entidade Promotora (Sociedade Brasileira de Computação - SBC).

- Criar o evento: Simpósio Brasileiro de Arquitetura de Software (SBCARS). Dados: Nome, Sigla (SBCARS), Entidade Promotora (SBC).

- Editar os dados de um evento existente.

- Deletar um evento.

## Tarefas e Responsáveis:

### Modelagem e Admin	
1. Criar/Refinar o Modelo Event: Garantir que o modelo em paperpaper/models.py tenha os campos nome, sigla, entidade_promotora e slug.

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

2. Configurar o Admin: Adicionar Event ao paperpaper/admin.py para permitir CRUD via interface administrativa (como fallback e verificação inicial).

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

### Backend/Views	
3. Criar a View event_create: Implementar a view e a lógica de formulário para a criação de novos eventos (@staff_member_required).

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

4. Criar a View event_edit: Implementar a view para carregar e atualizar eventos existentes (CRUD: Update).	[Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]
Backend/Views	5. Criar a View event_delete: Implementar a view de confirmação e a lógica de remoção de eventos (CRUD: Delete).	

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

### URLs
6. Configurar as Rotas: Adicionar as URLs create/, <slug>/edit/ e <slug>/delete/ em urls.py, mapeando-as para as views correspondentes.	

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

### Frontend/Templates	
7. Criar event_form.html: Implementar o template de formulário reutilizável para criação e edição de eventos.

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

8. Criar event_confirm_delete.html: Implementar o template de confirmação de exclusão.

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]

9. Atualizar events_list.html: Adicionar o botão "Novo Evento" e os botões de gerenciamento (Editar/Deletar) nos cards da lista, visíveis apenas para user.is_staff.	

    [Giovanni + Copilot - Agentic (Claude Sonnet 3.5)]
### Testes de Aceitação	

10. Testar CRUD Completo: Executar o teste de aceitação: criar SBES e SBCARS, editar SBCARS, e verificar a exclusão. 

    [Giovanni]
