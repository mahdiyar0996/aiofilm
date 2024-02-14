from django.test import TestCase, TransactionTestCase
from .models import User
from django.shortcuts import reverse
from django.db.utils import IntegrityError
from django.contrib.auth import login

class Mytest(TransactionTestCase):
    def setUp(self) -> None:
        print('tests are Running !!!')
        self.u1 = User.objects.create_user(username='test1', email='test1@gmail.com', password='Test0996')
    def test_user_create(self):
        u1 = User.objects.get(pk=self.u1.pk)
        self.assertEqual(u1, self.u1)
        self.assertEqual(u1.is_superuser, False )
        self.assertEqual(u1.is_staff, False )
        self.assertEqual(u1.is_active, False )
    def test_register(self):
        response = self.client.get('/register', follow=True)
        response1 = self.client.post('/register', data={'username': 'test2',
                                                        "email": 'test2@gmail.com',
                                                        'password1': 'Test0996',
                                                        "password2": 'Test0996'})
        response2 = self.client.post('/register', data={'username': 'test3',
                                                        "email": 'test3@gmail.com',
                                                        'password1': 'test0996',
                                                        "password2": 'test0996'})
        u1 = User.objects.get(username='test2')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get("PATH_INFO"), '/register')
        self.assertEqual(response1.status_code, 200)
        self.assertEqual(u1.username, 'test2')
        with self.assertRaises(User.DoesNotExist):
            u2 = User.objects.get(username='test3')