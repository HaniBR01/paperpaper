# Configuração do Ambiente de Desenvolvimento com Conda

Este guia descreve como configurar e rodar o projeto `paperpaper` usando Conda e SQLite.

## Pré-requisitos

### Instalação do Conda

Se você não tem o Conda instalado, siga as instruções abaixo para sua plataforma:

#### Linux (Ubuntu/Debian/CentOS/RedHat)
```bash
# Baixar o Miniconda
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh

# Dar permissão de execução
chmod +x Miniconda3-latest-Linux-x86_64.sh

# Executar o instalador
./Miniconda3-latest-Linux-x86_64.sh

# Seguir as instruções do instalador (pressione Enter para aceitar defaults)
# Quando perguntado se deseja inicializar conda, digite 'yes'

# Recarregar o terminal
source ~/.bashrc

# Verificar instalação
conda --version
```

#### macOS
```bash
# Baixar o Miniconda
curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh

# Executar o instalador
bash Miniconda3-latest-MacOSX-x86_64.sh

# Seguir as instruções do instalador
# Quando perguntado se deseja inicializar conda, digite 'yes'

# Recarregar o terminal
source ~/.bash_profile
# ou se usar zsh:
source ~/.zshrc

# Verificar instalação
conda --version
```

#### Windows (PowerShell/Command Prompt)
```powershell
# Baixar o Miniconda (execute no PowerShell como Administrador)
Invoke-WebRequest -Uri "https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe" -OutFile "Miniconda3-latest-Windows-x86_64.exe"

# Executar o instalador
./Miniconda3-latest-Windows-x86_64.exe

# Seguir o assistente de instalação
# Marcar a opção "Add Miniconda3 to PATH environment variable"

# Reiniciar o terminal/PowerShell

# Verificar instalação
conda --version
```

### Configuração Inicial do Conda (Todos os Sistemas)
```bash
# Configurar canais recomendados
conda config --add channels conda-forge
conda config --set channel_priority strict

# Atualizar conda para a versão mais recente
conda update conda

# Verificar configuração
conda info
```

### Outros Pré-requisitos
- **Git**: Necessário para clonar o repositório
  - **Linux**: `sudo apt-get install git` (Ubuntu/Debian) ou `sudo yum install git` (CentOS/RedHat)
  - **macOS**: `brew install git` (com Homebrew) ou baixe do [site oficial](https://git-scm.com/)
  - **Windows**: Baixe do [site oficial](https://git-scm.com/)

---

## Passo a Passo

### 1. Clonar o Repositório (se necessário)

Se você ainda não tem o projeto, clone o repositório do GitHub:

```bash
git clone git@github.com:HaniBR01/paperpaper.git
cd paperpaper
```

### 2. Criar o Ambiente Conda

Crie e ative o ambiente conda usando o arquivo `environment.yml`:

```bash
conda env create -f environment.yml
conda activate paperpaper
```

### 3. Aplicar as Migrações do Banco de Dados

```bash
python manage.py migrate
```

### 4. Criar um Superusuário

```bash
python manage.py createsuperuser
```

### 5. Configurar Permissões do Sistema (Opcional)

Para configurar grupos de usuários e permissões automaticamente:

```bash
python manage.py shell < setup_permissions.py
```

Este comando criará:
- **Grupo "Administradores"**: Acesso total ao sistema
- **Grupo "Usuários"**: Apenas visualização

### 6. Iniciar o Servidor de Desenvolvimento

```bash
python manage.py runserver
```

### 7. Acessar a Aplicação

O servidor estará disponível em `http://localhost:8000/`.

**Para acessar o painel administrativo:**
- URL: `http://localhost:8000/admin/`
- Use as credenciais do superusuário criado

---

## Gerenciamento de Usuários e Permissões

### Atribuir usuários aos grupos:

1. Acesse o Django Admin (`http://localhost:8000/admin/`)
2. Vá em **"Usuários"** → Selecione um usuário
3. Na seção **"Grupos"**, adicione o usuário ao grupo desejado:
   - **Administradores**: Para usuários com acesso total
   - **Usuários**: Para usuários com acesso apenas de visualização

### Criar novos usuários:

1. No Django Admin, vá em **"Usuários"** → **"Adicionar usuário"**
2. Preencha username e senha
3. Após salvar, edite o usuário para adicionar informações extras
4. Atribua ao grupo apropriado

---

## Comandos Úteis

### Conda
- **Desativar o ambiente conda:**
  ```bash
  conda deactivate
  ```

- **Reativar o ambiente:**
  ```bash
  conda activate paperpaper
  ```

- **Atualizar dependências:**
  ```bash
  conda env update -f environment.yml
  ```

- **Listar ambientes disponíveis:**
  ```bash
  conda env list
  ```

- **Remover ambiente (se necessário):**
  ```bash
  conda env remove -n paperpaper
  ```

- **Exportar ambiente atual:**
  ```bash
  conda env export > environment.yml
  ```

### Django
- **Configurar permissões do sistema:**
  ```bash
  python manage.py shell < setup_permissions.py
  ```

- **Acessar o shell do Django:**
  ```bash
  python manage.py shell
  ```

- **Executar testes:**
  ```bash
  python manage.py test
  ```

- **Coletar arquivos estáticos:**
  ```bash
  python manage.py collectstatic
  ```

- **Criar migrações após alterações no modelo:**
  ```bash
  python manage.py makemigrations
  ```

- **Aplicar migrações:**
  ```bash
  python manage.py migrate
  ```

---

## Resolução de Problemas Comuns

### Problema: Conda não é reconhecido como comando
**Solução:**
```bash
# Linux/macOS
echo 'export PATH="$HOME/miniconda3/bin:$PATH"' >> ~/.bashrc
source ~/.bashrc

# Windows (adicionar ao PATH manualmente ou reinstalar)
# Reinstale o Miniconda marcando "Add to PATH" durante instalação
```

### Problema: Ambiente não ativa
**Solução:**
```bash
# Verificar se o conda está funcionando
conda info

# Inicializar conda shell (se necessário)
conda init bash  # Linux/macOS
conda init powershell  # Windows

# Reiniciar terminal e tentar novamente
conda activate paperpaper
```

### Problema: Dependências não instaladas corretamente
**Solução:**
```bash
# Remover e recriar ambiente
conda env remove -n paperpaper
conda env create -f environment.yml
conda activate paperpaper
```

### Problema: Porta 8000 já em uso
**Solução:**
```bash
# Usar porta diferente
python manage.py runserver 8001

# Ou encontrar e matar processo na porta 8000
# Linux/macOS:
lsof -ti:8000 | xargs kill -9

# Windows:
netstat -ano | findstr :8000
taskkill /PID <PID_NUMBER> /F
```

### Problema: Erro de permissões no banco de dados
**Solução:**
```bash
# Verificar permissões do arquivo db.sqlite3
ls -la db.sqlite3

# Corrigir permissões (Linux/macOS)
chmod 664 db.sqlite3

# Recriar banco se necessário
rm db.sqlite3
python manage.py migrate
python manage.py createsuperuser
```

---

## Observações

- O banco de dados SQLite será criado automaticamente como `db.sqlite3` na raiz do projeto.
- O banco de dados **está incluído no repositório** para facilitar o desenvolvimento colaborativo.
- Para desenvolvimento, o SQLite é suficiente. Para produção, considere usar PostgreSQL ou MySQL.
- Execute o script de permissões sempre que configurar um novo ambiente ou resetar o banco de dados.
