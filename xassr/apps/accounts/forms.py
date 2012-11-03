# -*- encoding:utf-8 -*-
from django import forms
from django.forms import widgets
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class XassrUserCreationForm(UserCreationForm):
    username = forms.CharField(label=u'ユーザーID', help_text=u'空白を含めない英数字、記号で入力してください。')
    screen_name = forms.CharField(label=u'表示名', required=True)
    password1 = forms.CharField(label=u'パスワード', widget=widgets.PasswordInput())

    class Meta(UserCreationForm.Meta):
        fields = ('username', 'screen_name', 'email', 'password1', 'password2')

    def save(self, commit=True, token_generator=default_token_generator):
        user = super(XassrUserCreationForm, self).save(commit=False)
        if commit:
            user.screen_name = self.cleaned_data['screen_name']
            user.token = token_generator.make_token(user)
            user.save()
        return user

    def clean_email(self):
        value = self.cleaned_data['email']
        count = User.objects.filter(email=value).count()
        if count > 0:
            raise forms.ValidationError(u'このメールアドレスは既に使われています。')
        else:
            return value

    def clean_username(self):
        value = self.cleaned_data['username']
        if ' ' in value:
            raise forms.ValidationError(u'ユーザーIDは空白を含めない英数字、記号で入力してください。')
        else:
            return value
