# -*- encoding:utf-8 -*-
from django.conf.urls import patterns, url


# See: https://docs.djangoproject.com/en/dev/topics/http/urls/
urlpatterns = patterns('',
    url(r'^signup/$', 'xassr.apps.accounts.views.signup'),
    url(r'^verify/(?P<token>.+)/$', 'xassr.apps.accounts.views.verify'),
)