#!/usr/bin/env python
"""
テストユーザー作成スクリプト
"""

import os
import django
import sys

# Djangoの設定
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'school_project.settings')
django.setup()

from school_management.models import CustomUser

def create_test_users():
    """テスト用ユーザーを作成"""
    
    # 教員ユーザー作成
    if not CustomUser.objects.filter(email='teacher@test.com').exists():
        teacher = CustomUser.objects.create_user(
            email='teacher@test.com',
            full_name='テスト教員',
            password='teacher123',
            role='teacher',
            teacher_id='T001'
        )
        print(f'教員ユーザーを作成しました: {teacher.email}')
    else:
        print('教員ユーザーは既に存在します')
    
    # 学生ユーザー作成
    students_data = [
        ('student1@test.com', '田中太郎', 'S001'),
        ('student2@test.com', '佐藤花子', 'S002'),
        ('student3@test.com', '山田次郎', 'S003'),
        ('student4@test.com', '鈴木美香', 'S004'),
    ]
    
    for email, name, student_number in students_data:
        if not CustomUser.objects.filter(email=email).exists():
            student = CustomUser.objects.create_user(
                email=email,
                full_name=name,
                password='student123',
                role='student',
                student_number=student_number
            )
            print(f'学生ユーザーを作成しました: {student.email} ({student.full_name})')
        else:
            print(f'学生ユーザーは既に存在します: {email}')

if __name__ == '__main__':
    create_test_users()
    print('\nテストユーザー作成完了！')
    print('\n=== ログイン情報 ===')
    print('管理者: admin@admin.com / admin')
    print('教員: teacher@test.com / teacher123')  
    print('学生: student1@test.com / student123')
    print('学生: student2@test.com / student123')
    print('学生: student3@test.com / student123')
    print('学生: student4@test.com / student123')
