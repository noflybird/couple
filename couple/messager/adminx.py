#!/usr/bin/env python
# encoding: utf-8


import xadmin
from couple.messager.models import Message


class MessagesAdmin(object):
    list_display = ['sender', 'recipient', "message"]


xadmin.site.register(xadmin, MessagesAdmin)
