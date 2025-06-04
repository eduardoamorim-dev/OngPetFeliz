# Criação de Conta Administrativa

## Como criar uma conta de administrador

Para acessar o painel administrativo, você precisa criar uma conta de administrador usando o Django shell.

### 1. Acesse o shell do Django

```bash
python manage.py shell
```

### 2. Crie o usuário administrador

```python
from django.contrib.auth.models import User

# Criar superusuário
admin_user = User.objects.create_superuser(
    username='admin',
    email='admin@ongpetfeliz.com',
    password='suasenhasegura123'
)

print(f"Usuário administrador '{admin_user.username}' criado com sucesso!")
```

### 3. (Opcional) Criar usuário staff

Se você quiser criar um usuário com permissões limitadas:

```python
from django.contrib.auth.models import User

# Criar usuário staff
staff_user = User.objects.create_user(
    username='funcionario',
    email='funcionario@ongpetfeliz.com',
    password='outrasenhasegura123'
)

# Dar permissões de staff
staff_user.is_staff = True
staff_user.save()

print(f"Usuário staff '{staff_user.username}' criado com sucesso!")
```

### 4. Acesso ao sistema

Após criar a conta, você pode acessar:

- **Painel Administrativo**: http://localhost:5000/gestao/
- **Login**: http://localhost:5000/gestao/login/

### 5. Alterar senha (se necessário)

```python
from django.contrib.auth.models import User

# Encontrar o usuário
user = User.objects.get(username='admin')

# Alterar senha
user.set_password('novasenha123')
user.save()

print("Senha alterada com sucesso!")
```

### 6. Verificar usuários existentes

```python
from django.contrib.auth.models import User

# Listar todos os usuários
users = User.objects.all()
for user in users:
    print(f"Usuário: {user.username} | Email: {user.email} | Staff: {user.is_staff} | Superuser: {user.is_superuser}")
```

## Recursos do Painel Administrativo

- **Dashboard**: Estatísticas e resumo geral
- **Gestão de Cães**: Adicionar, editar e gerenciar perfis de cães
- **Solicitações de Adoção**: Aprovar/rejeitar pedidos de adoção
- **Candidatos a Voluntário**: Gerenciar aplicações de voluntariado
- **Mensagens de Contato**: Responder mensagens do site
- **Depoimentos**: Gerenciar testemunhos de adotantes

## Segurança

- Use senhas fortes (mínimo 12 caracteres)
- Não compartilhe credenciais
- Faça logout sempre que terminar de usar o sistema
- Mantenha o sistema atualizado

## Suporte

Em caso de problemas com o acesso administrativo:

1. Verifique se o usuário foi criado corretamente
2. Confirme se `is_staff=True` está definido
3. Teste o login no painel
4. Verifique os logs do Django para erros
