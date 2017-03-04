# -*- coding: utf-8 -*-
from models import Blog
from django.http import Http404, HttpResponseRedirect


def no_repeat(fuc):
    def wrapper(request):
        blog_list = Blog.objects.filter(title=request.POST['title'])
        if len(blog_list) == 0:
            return fuc(request)
        else:
            raise Http404()
    return wrapper


def is_login(fuc):
    def wrapper(*args, **kwargs):
        if args[0].user.is_authenticated():
            return fuc(*args, **kwargs)
        else:
            return HttpResponseRedirect('/main/')
    return wrapper