# Configuração do Banco PostgreSQL - ong_petfeliz

## Passo 1: Criar o arquivo .env

Crie um arquivo chamado `.env` na raiz do projeto (mesmo nível do manage.py) com o seguinte conteúdo:

```env
# Configurações do Banco de Dados PostgreSQL
DATABASE_URL=postgresql://seu_usuario:sua_senha@localhost:5432/ong_petfeliz
PGDATABASE=ong_petfeliz
PGUSER=seu_usuario
PGPASSWORD=sua_senha
PGHOST=localhost
PGPORT=5432

# Configurações do Django
DJANGO_SECRET_KEY=django-insecure-sua-chave-secreta-aqui
DEBUG=True
```

**IMPORTANTE:** Substitua os seguintes valores:
- `seu_usuario`: seu nome de usuário do PostgreSQL
- `sua_senha`: sua senha do PostgreSQL

## Passo 2: Configurar o Banco no PostgreSQL

### Opção A: Se o banco já existe
Se você já tem o banco `ong_petfeliz`, apenas configure as permissões:

```sql
-- Conecte ao PostgreSQL como superusuário
sudo -u postgres psql

-- Conceda permissões ao seu usuário
GRANT ALL PRIVILEGES ON DATABASE ong_petfeliz TO seu_usuario;
GRANT ALL ON SCHEMA public TO seu_usuario;
ALTER USER seu_usuario CREATEDB;

-- Sair
\q
```

### Opção B: Se precisa criar o banco
```sql
-- Conecte ao PostgreSQL como superusuário
sudo -u postgres psql

-- Criar o banco de dados
CREATE DATABASE ong_petfeliz;

-- Criar usuário (se não existir)
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';

-- Conceder privilégios
GRANT ALL PRIVILEGES ON DATABASE ong_petfeliz TO seu_usuario;
GRANT ALL ON SCHEMA public TO seu_usuario;
ALTER USER seu_usuario CREATEDB;

-- Sair
\q
```

## Passo 3: Testar a Conexão

```bash
# Teste a conexão diretamente
psql -h localhost -U seu_usuario -d ong_petfeliz

# Se conectar com sucesso, digite \q para sair
```

## Passo 4: Configurar o Projeto Django

```bash
# Instalar dependências (se ainda não instalou)
pip install django psycopg2-binary python-dotenv

# Fazer migrações
python manage.py makemigrations
python manage.py migrate

# Criar superusuário (opcional)
python manage.py createsuperuser

# Popular com dados de exemplo
python populate_data.py

# Iniciar o servidor
python manage.py runserver
```

## Passo 5: Verificar se Funcionou

```bash
# Verificar conexão com o banco
python manage.py check --database default

# Se não houver erros, o banco está configurado corretamente!
```

## Solução de Problemas

### Erro: "role does not exist"
```sql
-- Criar o usuário
CREATE USER seu_usuario WITH PASSWORD 'sua_senha';
```

### Erro: "database does not exist"
```sql
-- Criar o banco
CREATE DATABASE ong_petfeliz;
```

### Erro: "permission denied"
```sql
-- Conceder permissões
GRANT ALL PRIVILEGES ON DATABASE ong_petfeliz TO seu_usuario;
GRANT ALL ON SCHEMA public TO seu_usuario;
```

### Erro: "authentication failed"
- Verifique se a senha está correta no arquivo .env
- Verifique se o usuário existe no PostgreSQL

## Estrutura de Arquivos

Depois da configuração, seu projeto deve ter:
```
projeto/
├── .env                    # Suas variáveis de ambiente
├── .env.example           # Exemplo das variáveis
├── manage.py
├── dogs_rescue/
├── main/
├── templates/
├── static/
└── populate_data.py       # Script para popular o banco
```

## Comandos Úteis PostgreSQL

```bash
# Ver bancos de dados
\l

# Conectar a um banco específico
\c ong_petfeliz

# Ver tabelas
\dt

# Ver usuários
\du

# Sair do PostgreSQL
\q
```