#!/usr/bin/env python
"""
Script para migrar dados de bfcongressos para public
Execute: python migrate_to_public.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bfcongressos.settings')
django.setup()

from django.db import connection
from core.models import Usuario
import json

def export_usuarios():
    """Exporta usuários do schema bfcongressos"""
    print("Exportando usuários do schema bfcongressos...")

    with connection.cursor() as cursor:
        # Temporariamente mudar para bfcongressos
        cursor.execute("SET search_path TO bfcongressos, public")

        # Buscar todos os usuários
        usuarios = Usuario.objects.all()
        usuarios_data = []

        for user in usuarios:
            user_dict = {
                'username': user.username,
                'email': user.email,
                'password': user.password,  # já está hasheado
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_active': user.is_active,
                'is_staff': user.is_staff,
                'is_superuser': user.is_superuser,
                'date_joined': user.date_joined.isoformat(),
                'last_login': user.last_login.isoformat() if user.last_login else None,
            }

            # Campos customizados se existirem
            if hasattr(user, 'telefone'):
                user_dict['telefone'] = user.telefone
            if hasattr(user, 'foto_perfil'):
                user_dict['foto_perfil'] = user.foto_perfil.name if user.foto_perfil else None

            usuarios_data.append(user_dict)

        # Voltar para public
        cursor.execute("SET search_path TO public")

    print(f"✅ Exportados {len(usuarios_data)} usuários")
    return usuarios_data

def drop_schema_bfcongressos():
    """Remove schema bfcongressos"""
    print("\nRemovendo schema bfcongressos...")

    with connection.cursor() as cursor:
        cursor.execute("DROP SCHEMA IF EXISTS bfcongressos CASCADE")

    print("✅ Schema bfcongressos removido")

def run_migrations():
    """Executa migrations no schema public"""
    print("\nExecutando migrations no schema public...")

    import subprocess
    result = subprocess.run(['python', 'manage.py', 'migrate'], capture_output=True, text=True)

    if result.returncode == 0:
        print("✅ Migrations aplicadas com sucesso")
    else:
        print(f"❌ Erro ao aplicar migrations: {result.stderr}")
        return False

    return True

def import_usuarios(usuarios_data):
    """Importa usuários para o schema public"""
    print("\nImportando usuários para schema public...")

    from django.utils import timezone
    from datetime import datetime

    for user_dict in usuarios_data:
        # Converter datas
        date_joined = datetime.fromisoformat(user_dict['date_joined'])
        last_login = datetime.fromisoformat(user_dict['last_login']) if user_dict['last_login'] else None

        # Criar usuário
        user = Usuario(
            username=user_dict['username'],
            email=user_dict['email'],
            password=user_dict['password'],  # já hasheado
            first_name=user_dict['first_name'],
            last_name=user_dict['last_name'],
            is_active=user_dict['is_active'],
            is_staff=user_dict['is_staff'],
            is_superuser=user_dict['is_superuser'],
            date_joined=date_joined,
            last_login=last_login,
        )

        # Campos customizados
        if 'telefone' in user_dict:
            user.telefone = user_dict['telefone']
        if 'foto_perfil' in user_dict and user_dict['foto_perfil']:
            user.foto_perfil = user_dict['foto_perfil']

        user.save()
        print(f"  ✅ Importado: {user.username}")

    print(f"✅ {len(usuarios_data)} usuários importados")

def main():
    print("=" * 60)
    print("MIGRAÇÃO DE DADOS: bfcongressos → public")
    print("=" * 60)

    # 1. Exportar usuários
    usuarios_data = export_usuarios()

    if not usuarios_data:
        print("\n⚠️  Nenhum usuário encontrado em bfcongressos")
        print("Você pode pular para o passo 2")
        response = input("\nContinuar mesmo assim? (s/n): ")
        if response.lower() != 's':
            return

    # 2. Dropar schema bfcongressos
    drop_schema_bfcongressos()

    # 3. Rodar migrations (cria tabelas no public)
    if not run_migrations():
        print("\n❌ Falha ao executar migrations. Abortando.")
        return

    # 4. Importar usuários
    if usuarios_data:
        import_usuarios(usuarios_data)

    print("\n" + "=" * 60)
    print("✅ MIGRAÇÃO CONCLUÍDA COM SUCESSO!")
    print("=" * 60)
    print("\nAgora você pode:")
    print("1. Rebuild da imagem Docker")
    print("2. Deploy no Portainer")
    print("3. Fazer login normalmente")

if __name__ == '__main__':
    main()
