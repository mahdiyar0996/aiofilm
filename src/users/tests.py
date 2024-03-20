from django.test import TestCase, TransactionTestCase
from .models import User
from django.shortcuts import reverse
from django.db.utils import IntegrityError
from django.contrib.auth import login
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from .tokens import email_verification_token
from threading import Thread
from django.contrib import messages
from django.test import Client
import requests


class Mytest(TransactionTestCase):
    def setUp(self) -> None:
        self.u1 = User.objects.create_user(username='test1', email='test1@gmail.com', password='Test0996')
        self.u7 = User.objects.create_user(username='test7', email='test7@gmail.com', password='Test0996', is_active=True)

    def test_user_create(self):
        u1 = User.objects.get(pk=self.u1.pk)
        self.assertEqual(u1, self.u1)
        self.assertEqual(u1.is_superuser, False )
        self.assertEqual(u1.is_staff, False )
        self.assertEqual(u1.is_active, False )
        
    def test_register(self):
        response = self.client.get(reverse('register'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.request.get("PATH_INFO"), reverse('register'))
        
        response1 = self.client.post(reverse('register'), data={'username': 'test2',
                                                        "email": 'test2@gmail.com',
                                                        'password1': 'Test0996',
                                                        "password2": 'Test0996'})
        self.assertEqual(response1.status_code, 200)
        u1 = User.objects.get(username='test2')
        self.assertEqual(u1.username, 'test2')
        self.assertEqual(u1.ipaddress, '127.0.0.1')
        
        response2 = self.client.post(reverse('register'), data={'username': 'test3',
                                                        "email": 'test3@gmail.com',
                                                        'password1': 'test0996',
                                                        "password2": 'test0996'})
        response3 = self.client.post(reverse('register'), data={'username': 'test4 test4',
                                                        "email": 'test4@gmail.com',
                                                        'password1': 'Test0996',
                                                        "password2": 'Test0996'})
        with self.assertRaises(User.DoesNotExist):
            User.objects.get(username='test3')
            User.objects.get(username='test4')
            
    def test_user_activate(self):
        u1 = User.objects.create_user(username='test5', email='test5@gmail.com', password='Test0996')
        uid = urlsafe_base64_encode(force_bytes(u1.pk))
        token = email_verification_token.make_token(u1)
        
        response = self.client.get(reverse('user-activate', args=[uid,token]), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('login'))
    
    def test_reset_password(self):
        response = self.client.get(reverse('password-recovery'))
        self.assertEqual(response.status_code, 200)
        
        # response2 = self.client.post(reverse('password-recovery'), {'email': 'test1@gmail.com'})
        # self.assertEqual(response2.status_code, 302)
        
        response3 = self.client.post(reverse('password-recovery'), {'email': 'testttttttttttttt@gmail.com'})
        self.assertEqual(response3.status_code, 400)
        
    
    def test_reset_password_complete(self):
        u1 = User.objects.create_user(username='test5', email='test5@gmail.com', password='Test0996')
        uid = urlsafe_base64_encode(force_bytes(u1.pk))
        token = email_verification_token.make_token(u1)
        
        response = self.client.get(reverse('password-recovery-complete', args=[uid, token]))
        self.assertEqual(response.status_code, 200)
        
        response2 = self.client.get(reverse('password-recovery-complete', args=[uid, 'dfsdfsd']))
        self.assertEqual(response2.status_code, 404)

        response = self.client.post(reverse('password-recovery-complete', args=[uid, token]),
                                    data={'password1': 'Test0070',
                                          "password2": "Test0070"})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))
        u1 = User.objects.get(username='test5')
        self.assertEqual(u1.check_password('Test0070'), True)
        
        u3 = User.objects.create_user(username='test6', email='test6@gmail.com', password='Test0996')
        uid = urlsafe_base64_encode(force_bytes(u3.pk))
        token = email_verification_token.make_token(u3)
        response3 = self.client.post(reverse('password-recovery-complete', args=[uid, token]),
                                     data={'password1': 'Test00000', 'password2': 'Test012121'})
        self.assertEqual(response3.status_code, 400)
        u2 = User.objects.get(username='test6')
        self.assertEqual(u2.check_password('Test0996'), True)
    
    def test_login(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        
        response2 = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'Test0996'})
        self.assertEqual(response2.status_code, 302)
        self.assertEqual(response2.url, '/panel/')
        
        response3 = self.client.post(reverse('login'), data={'username': 'test1', 'password': 'Test09966'})
        self.assertEqual(response3.status_code, 400)
    
    def test_panel(self):
        self.client.login(username='test1', password='Test0996')
        response1 = self.client.get(reverse('user-panel'))
        self.assertEqual(response1.status_code, 302)
        
        
        self.client.login(username='csad2wsxzczdfsafsfds', password='Test0996')
        response2 = self.client.get(reverse('user-panel'))
        self.assertEqual(response2.status_code, 302)
        
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('user-panel'))
        self.assertEqual(response.status_code, 200)