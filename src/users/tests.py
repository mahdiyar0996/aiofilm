from django.test import TestCase, TransactionTestCase
from .models import User, TicketDetails, Ticket
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
        
    def test_notification_list_view(self):
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('notifications'))
        self.assertEqual(response.status_code, 200)
        self.client.logout()
        response1 = self.client.get(reverse('notifications'))
        self.assertEqual(response1.status_code, 302)
        
    def test_panel_change_password(self):
        self.client.login(username='test7', password='Test0996')
        
        response = self.client.get(reverse('change-password'))
        self.assertEqual(response.status_code, 200)
        
        response1 = self.client.post(reverse('change-password'), data={'password': "Test0996",'password1': "NewPassword1", "password2": "NewPassword1"})
        self.assertEqual(response1.status_code, 200)
        u1 = User.objects.get(username="test7")
        self.assertEqual(u1.check_password('NewPassword1'), True)
        
        self.client.login(username='test7', password="NewPassword1")
        
        response2 = self.client.post(reverse('change-password'), data={'password': "NewPassword1",'password1': "NewPassword", "password2": "NewPassword"})
        self.assertEqual(response2.status_code, 200)
        u2 = User.objects.get(username="test7")
        self.assertEqual(u2.check_password('NewPassword1'), True)

        response3 = self.client.post(reverse('change-password'), data={'password': "NewPassword1",'password1': "newpassword1", "password2": "newpassword1"})
        self.assertEqual(response2.status_code, 200)
        u3 = User.objects.get(username="test7")
        self.assertEqual(u3.check_password('NewPassword1'), True)
    
    def test_panel_edit_account_view(self):
        self.client.login(username='test7', password='Test0996')
        response1 = self.client.get(reverse('user-edit-account'))
        self.assertEqual(response1.status_code, 200)
        
        self.client.login(username='test7', password='Test0996')
        response2 = self.client.post(reverse('user-edit-account'), data={
            'username': "test8", 'avatar': '/src/media/users/7146123.jpg', 'sex': '1',
            'first_name': 'mahdiyar', 'last_name': 'azimi',
            'city': 'Esfahan', 'age': '21'
        })
        self.assertEqual(response2.status_code, 302)
        u3 = User.objects.get(username='test8')
        self.assertEqual(u3.email, 'test7@gmail.com')
        
        
    def test_ticket_list_view(self):
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('ticket-list'))
        self.assertEqual(response.status_code, 200)
        
    def test_ticket_details_view(self):
        u1 = User.objects.get(username='test7')
        t1 = Ticket.objects.create(department='پشتیبانی', user=u1, subject='تست')
        td1 = TicketDetails.objects.create(ticket=t1, user=u1, message='test', file='/src/media/users/1000_F_568027622_DgZfYnf1Xv2ncLvPSuYqZ7CfEuE7pBVL.jpg')
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('ticket-details', args=[td1.id,]))
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username='test7', password='Test0996')
        response1 = self.client.post(reverse('ticket-details', args=[td1.id,]), data={'message': 'test7', 'file': '/src/media/users/7146123.jpg'})
        td2 = TicketDetails.objects.get(message='test7', user=u1)
        self.assertEqual(td2.message, 'test7')
    
    def test_ticket_create_view(self):
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('ticket-create'))
        self.assertEqual(response.status_code, 200)
        
        self.client.login(username='test7', password='Test0996')
        response1 = self.client.post(reverse('ticket-create'), data={'department': 'پشتیبانی', 'subject': 'test7','message': 'test7'})
        u1 = User.objects.get(username='test7')
        td1 = TicketDetails.objects.get(message='test7', user=u1)
        t1 = Ticket.objects.get(id=td1.ticket.id, subject='test7')
        self.assertEqual(t1.subject, 'test7')
        self.assertEqual(td1.message, 'test7')
        
    def test_bookmark_view(self):
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('bookmarks'))
        self.assertEqual(response.status_code, 200)
    
    def test_favorite_view(self):
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('favorite'))
        self.assertEqual(response.status_code, 200)

    def test_favorite_view(self):
        self.client.login(username='test7', password='Test0996')
        response = self.client.get(reverse('comments'))
        self.assertEqual(response.status_code, 200)
        