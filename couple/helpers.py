# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from functools import wraps

from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    @wraps(f)
    def wrap(request, *args, **kwargs):
        if not request.is_ajax():
            return HttpResponseBadRequest("-不是ajax请求-")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequiredMixin(View):

    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied

        return super(AuthorRequiredMixin,self).dispatch(request, *args, **kwargs)
