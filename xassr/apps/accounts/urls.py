# -*- encoding:utf-8 -*-
from django.conf.urls import patterns, url


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    url(r'^signup/$', 'xassr.apps.accounts.views.signup'),
    url(r'^verify/(?P<token>.+)/$', 'xassr.apps.accounts.views.verify'),
    url(r'^signin/$', 'django.contrib.auth.views.login', {'template_name': 'accounts/signin.html'}),
    url(r'^signout/$', 'django.contrib.auth.views.logout_then_login', {'login_url': '/accounts/signin/'}),
)