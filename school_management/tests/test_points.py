from django.test import TestCase, Client
from django.urls import reverse
from school_management.models import CustomUser, ClassRoom, StudentClassPoints

class PointsAPITest(TestCase):
    def setUp(self):
        # 教員と学生ユーザー、クラスを作成
        self.teacher = CustomUser.objects.create_user(email='teacher@example.com', full_name='Teacher One', password='pass123', role='teacher')
        self.student = CustomUser.objects.create_user(email='student@example.com', full_name='Student One', password='pass123', role='student', student_number='S001')
        self.classroom = ClassRoom.objects.create(class_name='Test Class', year=2025, semester='first')
        self.classroom.teachers.add(self.teacher)
        self.classroom.students.add(self.student)

        # クライアントをログイン状態で用意（teacher）
        self.client = Client()
        self.client.force_login(self.teacher)

    def test_update_overall_points(self):
        url = reverse('school_management:update_student_points', kwargs={'student_id': self.student.id})
        data = {'points': 7}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.student.refresh_from_db()
        self.assertEqual(self.student.points, 7)

    def test_update_class_points(self):
        url = reverse('school_management:update_student_points', kwargs={'student_id': self.student.id})
        data = {'points': 12, 'class_id': self.classroom.id}
        response = self.client.post(url, data, content_type='application/json')
        self.assertEqual(response.status_code, 200)
        # StudentClassPoints が作成され、値が設定されていること
        scp = StudentClassPoints.objects.get(student=self.student, classroom=self.classroom)
        self.assertEqual(scp.points, 12)

    def test_update_points_via_student_edit_view(self):
        # 学生編集ページにPOSTして points を更新できるか
        url = reverse('school_management:student_edit', kwargs={'student_number': self.student.student_number})
        # 必須フィールドを含めたフォームデータ
        data = {
            'full_name': self.student.full_name,
            'furigana': 'フリガナ',
            'email': self.student.email,
            'points': '15'
        }
        response = self.client.post(url, data)
        # リダイレクトが発生すれば成功とみなす
        self.assertIn(response.status_code, (302, 200))
        self.student.refresh_from_db()
        self.assertEqual(self.student.points, 15)
