# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from django.urls import path
from django.views.decorators.cache import cache_page

from couple.articles.views import (ArticlesListView, CreateArticleView, DraftsListView,
                                   DetailArticleView, EditArticleView)

app_name = 'articles'

urlpatterns = [
    path('', ArticlesListView.as_view(), name='list'),
    path('write-new-article/', CreateArticleView.as_view(), name='write_new'),
    path('drafts/', DraftsListView.as_view(), name='drafts'),
    path('<str:slug>/', cache_page(60 * 5)(DetailArticleView.as_view()), name='article'),
    path('edit/<int:pk>/', EditArticleView.as_view(), name='edit_article'),
]
