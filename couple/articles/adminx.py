#!/usr/bin/env python
# encoding: utf-8
import xadmin
from couple.articles.models import Article


class ArticleAdmin(object):
    list_display = ["title", "edited", "content", "tags"]


xadmin.site.register(Article, ArticleAdmin)


