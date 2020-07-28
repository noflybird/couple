# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
import datetime
from haystack import indexes

from couple.news.models import News
from couple.articles.models import Article
from couple.qa.models import Question
from taggit.models import Tag
from django.contrib.auth import get_user_model

User = get_user_model()


class ArticleIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/article_text.txt')

    def get_model(self):
        return Article

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(status="P", updated_at__lte=datetime.datetime.now())


class NewsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/news_text.txt')

    def get_model(self):
        return News

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return self.get_model().objects.filter(reply=False, updated_at__lte=datetime.datetime.now())


class QuestionIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/questions_text.txt')

    def get_model(self):
        return Question

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())


class UserIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/users_text.txt')

    def get_model(self):
        return get_user_model()

    def index_queryset(self, using=None):
        return self.get_model().objects.filter(updated_at__lte=datetime.datetime.now())


class TagsIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True, template_name='search/tags_text.txt')

    def get_model(self):
        return Tag

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
