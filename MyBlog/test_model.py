# -*- coding: utf-8 -*-
from django.test import TestCase
from models import Blog, STATUS_ACTIVE, STATUS_DELETE
import datetime


class BlogTest(TestCase):

    def setUp(self):
        Blog.objects.create(title='first', \
                            content='123', \
                            create_time=datetime.datetime.now(), \
                            user_name='zxt', \
                            favor=0, \
                            status=STATUS_ACTIVE)

    def test_blog(self):
        first = Blog.objects.get(title='first')
        self.assertEqual(first.content, '123')

    def test_delete(self):
        first = Blog.objects.get(status=STATUS_ACTIVE)
        self.assertEqual(first.user_name, '123')
        first.status = STATUS_DELETE
        first.save()
        first = Blog.objects.get(status=STATUS_DELETE)
        self.assertIsNone(first)


