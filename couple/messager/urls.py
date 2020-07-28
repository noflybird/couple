# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from django.urls import path

from couple.messager.views import MessagesListView, send_message, ConversationListView

app_name = 'messager'

urlpatterns = [
    path('', MessagesListView.as_view(), name='messages_list'),
    path('send-message/', send_message, name='send_message'),
    path('<username>/', ConversationListView.as_view(), name='conversation_detail'),
]
