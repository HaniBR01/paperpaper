"""
Script para configurar grupos e permissões iniciais do sistema PaperPaper
Execute: python manage.py shell < setup_permissions.py
"""

from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from paperpaper.models import Event, Edition, Article, Author, NotificationSubscription, BibtexImport

# Criar grupos
admin_group, created = Group.objects.get_or_create(name='Administradores')
if created:
    print("Grupo 'Administradores' criado com sucesso")

user_group, created = Group.objects.get_or_create(name='Usuários')
if created:
    print("Grupo 'Usuários' criado com sucesso")

# Configurar permissões para Administradores (acesso total)
admin_permissions = [
    # Event
    'add_event', 'change_event', 'delete_event', 'view_event',
    # Edition
    'add_edition', 'change_edition', 'delete_edition', 'view_edition',
    # Article
    'add_article', 'change_article', 'delete_article', 'view_article',
    # Author
    'add_author', 'change_author', 'delete_author', 'view_author',
    # NotificationSubscription
    'add_notificationsubscription', 'change_notificationsubscription', 
    'delete_notificationsubscription', 'view_notificationsubscription',
    # BibtexImport
    'add_bibtexximport', 'change_bibtexximport', 'delete_bibtexximport', 'view_bibtexximport',
]

for perm_codename in admin_permissions:
    try:
        permission = Permission.objects.get(codename=perm_codename)
        admin_group.permissions.add(permission)
    except Permission.DoesNotExist:
        print(f"Permissão {perm_codename} não encontrada")

# Configurar permissões para Usuários (apenas visualização)
user_permissions = [
    'view_event', 'view_edition', 'view_article', 'view_author'
]

for perm_codename in user_permissions:
    try:
        permission = Permission.objects.get(codename=perm_codename)
        user_group.permissions.add(permission)
    except Permission.DoesNotExist:
        print(f"Permissão {perm_codename} não encontrada")

print("Configuração de permissões concluída!")
print("\nPara atribuir usuários aos grupos:")
print("1. Acesse o Django Admin")
print("2. Vá em 'Usuários' > Selecione um usuário")
print("3. Na seção 'Grupos', adicione o usuário ao grupo desejado")
print("\nGrupos disponíveis:")
print("- Administradores: Acesso total ao sistema")
print("- Usuários: Apenas visualização de conteúdo público")
