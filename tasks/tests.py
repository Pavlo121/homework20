from .forms import TaskForm
from rest_framework.test import APITestCase
from .serializers import TaskSerializer
from django.contrib.auth.models import User
from django.test import TestCase
from datetime import date, timedelta


class TaskFormTests(TestCase):
    def test_valid_form(self):
        form_data = {
            'title': 'Test Task',
            'description': 'Тест',
            'due_date': date.today() + timedelta(days=1)
        }
        form = TaskForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_empty_required_fields(self):
        form_data = {'description': 'description'}
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('due_date', form.errors)

    def test_due_date_in_past(self):
        form_data = {
            'title': 'Test Task',
            'description': 'Прострочений термін',
            'due_date': date.today() - timedelta(days=1)
        }
        form = TaskForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn('due_date', form.errors)


class TaskSerializerTests(APITestCase):
    def test_valid_serializer(self):
        data = {
            'title': 'Test Task',
            'description': 'Тест',
            'due_date': date.today() + timedelta(days=1)
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_missing_title(self):
        data = {
            'description': 'Відсутня назва',
            'due_date': date.today() + timedelta(days=1)
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('title', serializer.errors)

    def test_due_date_in_past(self):
        data = {
            'title': 'Завдання з минулою датою',
            'due_date': date.today() - timedelta(days=1)
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('due_date', serializer.errors)


class ExtendedTaskSerializerTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', email='test@example.com')

    def test_valid_serializer_with_user(self):
        data = {
            'user': self.user.id,
            'title': 'Завдання з користувачем',
            'description': 'Тестове завдання з даними користувача',
            'due_date': date.today() + timedelta(days=1)
        }
        serializer = TaskSerializer(data=data)
        self.assertTrue(serializer.is_valid())

    def test_invalid_user_data(self):
        data = {
            'user': {
                'username': '',
                'email': 'invalid-email'
            },
            'title': 'Завдання с invalid user',
            'due_date': date.today() + timedelta(days=1)
        }
        serializer = TaskSerializer(data=data)
        self.assertFalse(serializer.is_valid())
        self.assertIn('user', serializer.errors)
