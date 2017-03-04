# -*- coding: utf-8 -*-
from models import Tags, Blog
from blog_data import TagData
from collections import OrderedDict

ACCOUNT = 'lan4627@gmail.com'

def get_tag_data_list():
    tag_data_list = []
    tags = Tags.objects.filter(id__gt=0)
    for tag in tags:
        tag_data_list.append(
            TagData(
                tag.name+"-tag",
                tag.name,
                OrderedDict([(blog.title, blog.id) for blog in Blog.objects.filter(user_name=ACCOUNT, tag=tag.name)])))
    return tag_data_list

def get_tag_list():
    return Tags.objects.filter(id__gt=0)

def get_blog_list(name):
    return Blog.objects.filter(user_name=name).order_by('-id')