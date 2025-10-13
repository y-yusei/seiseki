"""
Railwayデプロイ時に管理者ユーザーを自動作成するスクリプト
環境変数でメールアドレスとパスワードを指定
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from school_management.models import CustomUser

# 環境変数から管理者情報を取得
ADMIN_EMAIL = os.environ.get('ADMIN_EMAIL', 'admin@example.com')
ADMIN_PASSWORD = os.environ.get('ADMIN_PASSWORD', 'admin123')
ADMIN_NAME = os.environ.get('ADMIN_NAME', '管理者')

# 既に存在する場合はスキップ
if not CustomUser.objects.filter(email=ADMIN_EMAIL).exists():
    CustomUser.objects.create_superuser(
        email=ADMIN_EMAIL,
        full_name=ADMIN_NAME,
        password=ADMIN_PASSWORD
    )
    print(f"✅ 管理者ユーザーを作成しました: {ADMIN_EMAIL}")
else:
    print(f"ℹ️  管理者ユーザーは既に存在します: {ADMIN_EMAIL}")
