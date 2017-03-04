# -*- coding: utf-8 -*-
from django.test import Client
from django.test.utils import setup_test_environment
from models import Blog
import datetime


def get_blog_list(blog_list, number):
    for n in range(0, number):
        blog = Blog(
            tag='test',
            title='test'+str(n),
            content='test_content'+str(n),
            create_time=datetime.datetime.now(),
            user_name='test_user',
            favor=0
        )
        blog_list.append(blog)
    return blog_list


def print_status_code(fuc):
    def get_wrapper(*args, **kwargs):
        print str(fuc.__name__) + ' : ' + str(fuc(*args, **kwargs))
    return get_wrapper


class AccountTest:

    def __init__(self):
        self.client = Client()

    @print_status_code
    def login(self):
        return self.client.post('/main/login/', {'username': 'lan4627@gmail.com', 'password': 'yx2.71828'}).status_code
        # response = self.client.get('/main/')
        # self.assertEqual(response.status_code, 200)

    @print_status_code
    def logout(self):
        return self.client.post('/main/logout/').status_code
        # self.assertEqual(response.status_code, 200)


class SubmitBlogTest:

    def __init__(self):
        self.client = Client()

    @print_status_code
    def submit(self, blog):
        return self.client.post('/write/submit-blog/', {'tag': blog.tag, 'title':  blog.title, 'content': blog.content}).status_code

    @print_status_code
    def save(self, blog):
        return self.client.post('/write/submit-blog/', {'tag': blog.tag, 'title':  blog.title, 'content': blog.content}).status_code

class DeleteBlogTest:

    def __init__(self):
        self.client = Client()

    @print_status_code
    def delete(self, blog):
        return self.client.post('/list/delete-blog/', {'title':  blog.title}).status_code


class FavorTest:

    def __init__(self):
        self.client = Client()

    @print_status_code
    def add(self, blog):
        return self.client.post('/main/favor/', {'title': blog.title, 'date':  blog.create_time, 'favor': 'true'}).status_code

    @print_status_code
    def reduce(self, blog):
        return self.client.post('/main/favor/', {'title': blog.title, 'date':  blog.create_time, 'favor': 'false'}).status_code


setup_test_environment()
blog_list = get_blog_list([], 2)
a = AccountTest()
s = SubmitBlogTest()
d = DeleteBlogTest()
f = FavorTest()
a.login()
for blog in blog_list:
    s.submit(blog)
    f.add(blog)
    f.reduce(blog)
    #d.delete(blog)
a.logout()