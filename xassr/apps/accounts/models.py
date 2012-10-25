# -*- encoding:utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

class XassrUserProfile(models.Model):
    user = models.ForeignKey(User, unique=True)
    screen_name = models.CharField(max_length=30)
    token = models.CharField(max_length=50)
    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __unicode__(self):
        return self.screen_name


def create_user_profile(sender, instance, created, **kwargs):
    """
    if user is created (or changed),
    then create user profile about the user, using signal

    kwargs contains such key 'raw', 'signal', 'using'
    """
    if created:
        # user is created, not changed
        data = {'user': instance}
        if hasattr(instance, 'screen_name'):
            data['screen_name'] = instance.screen_name
        if hasattr(instance, 'token'):
            data['token'] = instance.token
        XassrUserProfile.objects.create(**data)

post_save.connect(create_user_profile, sender=User)