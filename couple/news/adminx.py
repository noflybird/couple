#!/usr/bin/env python
# encoding: utf-8


import xadmin
from couple.news.models import News


class NewsAdmin(object):
    list_display = ['content']


xadmin.site.register(News, NewsAdmin)
