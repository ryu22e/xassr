# -*- encoding:utf-8 -*-
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import Context
from django.template.loader import get_template
from django.contrib.sites.models import get_current_site
from django.contrib.auth.models import User
from xassr.apps.accounts.forms import XassrUserCreationForm

def signup(request):
    if request.method == 'POST':
        form = XassrUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            user_profile = user.get_profile()
            t = get_template('accounts/mail/signup.html')
            current_site = get_current_site(request)
            site_name = current_site.name
            c = {
                'screen_name': user_profile.screen_name,
                'is_secure': request.is_secure(),
                'site_name': current_site.name,
                'token': user_profile.token,
            }
            user.email_user(u"メールアドレスのご確認", t.render(Context(c)))
            return HttpResponseRedirect('/')
    else:
        form = XassrUserCreationForm()

    c = RequestContext(request, {'form': form})
    return render_to_response('accounts/signup.html', c)


def verify(request, token):
    message = u"メールアドレスが確認できませんでした。"
    try:
        user = User.objects.filter(xassruserprofile__token__exact=token).get()
    except User.DoesNotExist:
        return HttpResponseRedirect('/')
    else:
        if user.is_active:
            user_profile = user.get_profile()
            user_profile.verified = True
            user_profile.save()
            message = u"メールアドレスが確認されました。"

    c = RequestContext(request, {'message': message})
    return render_to_response('accounts/verify.html', c)