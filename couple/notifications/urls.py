# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from django.urls import path

from couple.notifications.views import NotificationUnreadListView, mark_all_as_read, mark_as_read, get_latest_notifications

app_name = 'notifications'

urlpatterns = [
    path('', NotificationUnreadListView.as_view(), name='unread'),
    path('mark-as-read/<slug>/', mark_as_read, name='mark_as_read'),
    path('mark-all-as-read/', mark_all_as_read, name='mark_all_read'),
    path('latest-notifications/', get_latest_notifications, name='latest_notifications'),
]
