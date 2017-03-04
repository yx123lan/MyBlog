# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Blog
import datetime


class BlogTest(TestCase):

    def setUp(self):
        Blog.objects.create(title='first', content='123', create_time=datetime.datetime.now(), favor=0)


    def test_blog(self):
        first = Blog.objects.get(title='first')
        self.assertEqual(first.content, '123')


