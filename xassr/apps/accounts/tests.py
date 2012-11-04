# -*- encoding:utf-8 -*-
"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.core import mail
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.models import User
from xassr.apps.accounts.models import XassrUserProfile

class AccountsTest(TestCase):
    def test_signup(self):
        """
        Tests that signup is done.
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
        self.assertIsNotNone(p.token)
        self.assertIsNotNone(p.created_at)
        self.assertEqual(p.screen_name, data['screen_name'])
        self.assertEqual(len(mail.outbox), 1)
        outbox = mail.outbox[0]
        self.assertEqual(outbox.to, [data['email']])
        self.assertIsNotNone(outbox.from_email)
        self.assertEqual(outbox.subject, u'メールアドレスのご確認')

    def test_signup_username_contains_whitespace(self):
        """
         Tests that username contains whitespace is not accepted.
        """
        data = {
            'screen_name': 'Taro YAMADA',
            'username': 't yamada',
            'password1': 'password',
            'password2': 'password',
            'email': 'test@ryu22e.org',
        }
        r = self.client.post('/accounts/signup/', data)
        self.assertFormError(r, 'form', 'username', u'ユーザーIDは空白を含めない英数字、記号で入力してください。')

    def test_signup_duplicated_email(self):
        """
        Tests that duplicated email is not accepted.
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

    def test_verify_email(self):
        """
        Tests that verify email is done.
        """
        user = User.objects.create_user(username='test')
        token = default_token_generator.make_token(user)
        user.save()
        user_profile = user.get_profile()
        self.assertIsNotNone(user_profile)
        user_profile.token = token
        user_profile.save()

        r = self.client.get('/accounts/verify/{0}/'.format(token))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, u'メールアドレスが確認されました。')
        user_profile2 = XassrUserProfile.objects.filter(token=token).get()
        self.assertIsNotNone(user_profile2)
        self.assertEqual(user_profile2.verified, True)

    def test_verify_email_with_wrong_token(self):
        """
        Tests that wrong token is not accepted.
        """
        r = self.client.get('/accounts/verify/{0}/'.format('wrong_token'))
        self.assertRedirects(r, '/')

    def test_verify_email_not_active_user(self):
        """
        Tests verify with invalid token.
        """
        user = User.objects.create_user(username='test')
        user.is_active = False
        token = default_token_generator.make_token(user)
        user.save()
        user_profile = user.get_profile()
        self.assertIsNotNone(user_profile)
        user_profile.token = token
        user_profile.save()

        r = self.client.get('/accounts/verify/{0}/'.format(token))
        self.assertEqual(r.status_code, 200)
        self.assertContains(r, u'メールアドレスが確認できませんでした。')