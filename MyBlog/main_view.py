# -*- coding: utf-8 -*-
import logging
import json
import datetime
import re

from django.http import HttpResponse, HttpResponseRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.template import Template, Context, loader
from django.views.decorators.csrf import csrf_exempt
from django.contrib import auth

from markdown2 import markdown
from models import Blog, StoreBlog
from blog_checked import no_repeat, is_login
from db_helper import get_tag_data_list, get_tag_list, get_blog_list

FIRST_BLOG = -1
PAGE_SIZE = 15
SHORT_CONTENT_LENGTH = 250
MAIN_ACCOUNT = 'lan4627@gmail.com'
RESULT_STATUS_SUCCESS = 'suc'
RESULT_STATUS_FAILURE = 'fai'
RESULT_STATUS = 'status'
RESULT_URL = 'url'

logger = logging.getLogger(__name__)


def main(request):
    return read_blog(request, FIRST_BLOG)


def read_blog(request, blog_id):
    if blog_id is FIRST_BLOG:
        blog_list = Blog.objects.filter(user_name=MAIN_ACCOUNT).order_by('-id')[0:2]
        first_blog = blog_list[0]
        if len(blog_list) > 1:
            html = get_main_html(request, first_blog, 0, blog_list[1].id)
        else:
            html = get_main_html(request, first_blog)
    else:
        try:
            current_blog = Blog.objects.get(user_name=MAIN_ACCOUNT, id=blog_id)
        except ObjectDoesNotExist:
            raise Http404()
        positive_blog = Blog.objects.filter(user_name=MAIN_ACCOUNT, id__gt=blog_id)[0:1]
        next_blog = Blog.objects.filter(user_name=MAIN_ACCOUNT, id__lt=blog_id).order_by('-id')[0:1]
        html = get_main_html(request, current_blog, get_first_id(positive_blog) , get_first_id(next_blog))
    return HttpResponse(html)


def get_first_id(blog_list):
    return blog_list[0].id if len(blog_list) > 0 else 0


def all_blog_list(request, page_num):
    current_page = int(page_num)
    start = PAGE_SIZE * current_page
    end = PAGE_SIZE * (current_page + 1)
    blog_list_all = get_blog_list(MAIN_ACCOUNT)
    blog_list = blog_list_all[start:end]
    for blog in blog_list:
        content_str = blog.content
        code_pre_list = re.findall('```[\w\W]+?```', content_str)
        for code_pre in code_pre_list:
            content_str = content_str.replace(code_pre, '')
        blog.content = content_str[:SHORT_CONTENT_LENGTH] + ('...' if len(content_str) > SHORT_CONTENT_LENGTH else '')
    property_list = {
        'is_login': request.user.is_authenticated(),
        'blog_list': blog_list,
        'type_list': True,
        'first_blog_id': blog_list[0].id,
        'current_page': current_page,
        'page_num': len(blog_list_all) / PAGE_SIZE - current_page,
        'previous': current_page - 1,
        'next': current_page + 1
    }
    html = loader.get_template("allblog.html").render(Context(property_list))
    return HttpResponse(html)


@csrf_exempt
def login(request):
    data = request.POST
    user = auth.authenticate(username=data['username'], password=data['password'])
    if user is not None and user.is_active:
        auth.login(request, user)
        status = RESULT_STATUS_SUCCESS
    else:
        status = RESULT_STATUS_FAILURE
    logger.info('login '+ status)
    return HttpResponse(json.dumps({RESULT_STATUS: status}))


@csrf_exempt
def logout(request):
    auth.logout(request)
    return HttpResponse(json.dumps({RESULT_STATUS: RESULT_STATUS_SUCCESS}))


@csrf_exempt
@is_login
def write(request):
    return make_write_page()


def make_write_page(current_tag=None, current_title=None, current_content=None):
    t = loader.get_template("write.html")
    property_list = {
        'is_login': True,
        'tag_list': get_tag_list(),
        'current_tag': current_tag,
        'current_title': current_title,
        'current_content': current_content
    }
    return HttpResponse(t.render(Context(property_list)))


@csrf_exempt
@is_login
def submit_blog(request):
    data = request.POST
    blog_list = Blog.objects.filter(title=request.POST['title'])
    if len(blog_list) > 0:
        blog = blog_list[0]
        blog.tag = data['tag']
        blog.title = data['title']
        blog.content = data['content']
    else:
        blog = Blog(
            tag=data['tag'],
            title=data['title'],
            content=data['content'],
            create_time=datetime.datetime.now(),
            user_name=request.user.username,
            favor=0
        )
    try:
        blog.save()
        return HttpResponse(json.dumps({RESULT_STATUS: RESULT_STATUS_SUCCESS, RESULT_URL: '/main/' + blog.id + '/'}))
    except ValueError:
        logger.error('save blog error tag=' + data['tag'] + ' title=' + data['title'] + ' content=' + data['content'])
        return HttpResponse(json.dumps({RESULT_STATUS: RESULT_STATUS_FAILURE}))


@csrf_exempt
@is_login
def save_blog(request):
    if request.is_ajax():
        data = request.POST
        logger.info('save blog ' + data['title'])
        store_blog = StoreBlog(
            tag=data['tag'],
            title=data['title'],
            content=data['content'],
            user_name=request.user.username
        )
        try:
            store_blog.save()
            status = RESULT_STATUS_SUCCESS
        except ValueError:
            logger.error('save blog error')
            status = RESULT_STATUS_FAILURE
    else:
        status = RESULT_STATUS_FAILURE
    return HttpResponse(json.dumps({RESULT_STATUS: status}))


@csrf_exempt
@is_login
def delete_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        blog.delete()
        status = RESULT_STATUS_SUCCESS
    except ObjectDoesNotExist:
        status = RESULT_STATUS_FAILURE
    return HttpResponse(json.dumps({RESULT_STATUS: status}))


@is_login
def edit_blog(request, blog_id):
    try:
        blog = Blog.objects.get(id=blog_id)
        return make_write_page(blog.tag, blog.title, blog.content)
    except ObjectDoesNotExist:
        return Http404


@csrf_exempt
@is_login
def preview_blog(request):
    return HttpResponse(write_to_main_html(request))


# 由博客编写界面传入的数据来构建博客主页面
def write_to_main_html(request):
    data = request.POST
    blog = Blog()
    blog.id = 0
    blog.title = data['title']
    blog.content = data['content']
    blog.favor = 0
    blog.create_time = datetime.datetime.now()
    return get_main_html(request, blog)


def get_main_html(request, blog, previous_id=0, next_id=0):
    t = loader.get_template("main.html")
    blog_list = get_blog_list(MAIN_ACCOUNT)[0:5]
    property_len = {
        'title': blog.title,
        'create_date': blog.create_time,
        'content': markdown(blog.content, extras=['fenced-code-blocks']),
        'tag_list': get_tag_data_list(),
        'new_blogs': blog_list,
        'favor': blog.favor,
        'blog_id': blog.id,
        'previous_id': previous_id,
        'next_id': next_id,
        'is_login': request.user.is_authenticated(),
        'page_url': request.get_full_path(),
        'type_main': True
    }
    return t.render(Context(property_len))


@csrf_exempt
def blog_favor(request):
    data = request.POST
    logger.debug(data)
    blog = Blog.objects.get(id=data['id'])
    if 'true' == data['favor']:
        blog.favor += 1
    else:
        blog.favor -= 1
    try:
        blog.save()
        status = RESULT_STATUS_SUCCESS
    except ValueError:
        status = RESULT_STATUS_FAILURE
    return HttpResponse(json.dumps({RESULT_STATUS: status}))


@csrf_exempt
@is_login
def add_tag(request):
    return HttpResponse(json.dumps({RESULT_STATUS: RESULT_STATUS_SUCCESS}))


@csrf_exempt
def generate_204(request):
    return HttpResponse(status=204)

