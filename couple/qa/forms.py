# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from django import forms
from markdownx.fields import MarkdownxFormField

from couple.qa.models import Question


class QuestionForm(forms.ModelForm):
    status = forms.CharField(widget=forms.HiddenInput())  # 隐藏
    content = MarkdownxFormField()

    class Meta:
        model = Question
        fields = ["title", "content", "tags", "status"]
