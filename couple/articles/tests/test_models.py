# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from test_plus.test import TestCase

from couple.articles.models import Article


class ArticleModelTest(TestCase):

    def setUp(self):
        self.user = self.make_user("author1")

    def test_object_instance(self):
        pass

    def test_return_values(self):
        pass

