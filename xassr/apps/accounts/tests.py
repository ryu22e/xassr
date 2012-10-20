# -*- encoding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core import mail
from django.contrib.auth.models import User


class AccountsTest(TestCase):
    def test_signup(self):
        """
        Tests signup.
        """
        data = {
            'screen_name': 'Taro YAMADA',
            'username': 't_yamada',
            'password1': 'password',
            'password2': 'password',
            'email': 'test@ryu22e.org',
        }
        r = self.client.post('/accounts/signup/', data)
        self.assertRedirects(r, '/')
        u = User.objects.filter(username=data['username'])
        self.assertNotEqual(u, None)
        self.assertEqual(len(u), 1)
        p = u[0].get_profile()
        self.assertNotEqual(p, None)
        self.assertIsNotNone(p.created_at)
        self.assertEqual(p.screen_name, data['screen_name'])
        self.assertEqual(len(mail.outbox), 1)
        outbox = mail.outbox[0]
        self.assertEqual(outbox.to, [data['email']])
        self.assertIsNotNone(outbox.from_email)
        self.assertEqual(outbox.subject, u'メールアドレスのご確認')

    def test_signup_duplicated_email(self):
        """
        Test duplicated email.
        """
        data1 = {
            'screen_name': 'Taro YAMADA',
            'username': 't_yamada',
            'password1': 'password',
            'password2': 'password',
            'email': 'test@ryu22e.org',
        }
        r = self.client.post('/accounts/signup/', data1)
        self.assertRedirects(r, '/')
        u = User.objects.filter(username=data1['username'])
        self.assertNotEqual(u, None)
        self.assertEqual(len(u), 1)
        data2 = {
            'screen_name': 'Taro YAMADA',
            'username': 't_yamada',
            'password1': 'password',
            'password2': 'password',
            'email': 'test@ryu22e.org',
        }
        r = self.client.post('/accounts/signup/', data2)
        self.assertFormError(r, 'form', 'email', u'このメールアドレスは既に使われています。')