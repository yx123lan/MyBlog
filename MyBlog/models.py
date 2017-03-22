# -*- coding: utf-8 -*-
from django.db import models

USER_NAME_MAX_LENGTH = 30
USER_PASSWORD_MAX_LENGTH = 30
USER_NICKNAME_MAX_LENGTH = 30
TAG_MAX_LENGTH = 16
TITLE_MAX_LENGTH = 120
STATUS_DELETE = 1
STATUS_ACTIVE = 0


class Blog(models.Model):
    tag = models.CharField(u'tag', max_length=TAG_MAX_LENGTH)
    title = models.CharField(u'title', max_length=TITLE_MAX_LENGTH)
    content = models.TextField(u'content')
    create_time = models.DateField(u'create_time')
    user_name = models.CharField(u'user_name', max_length=USER_NAME_MAX_LENGTH)
    favor = models.IntegerField(u'favor', default=0)
    status = models.IntegerField(u'status', default=STATUS_ACTIVE)


class StoreBlog(models.Model):
    tag = models.CharField(u'tag', max_length=TAG_MAX_LENGTH, blank=True)
    title = models.CharField(u'title', max_length=TITLE_MAX_LENGTH, blank=True)
    content = models.TextField(u'content', blank=True)
    user_name = models.CharField(u'user_name', max_length=USER_NAME_MAX_LENGTH)


class Tags(models.Model):
    name = models.CharField(u'name', max_length=TAG_MAX_LENGTH)

