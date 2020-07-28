# -*- coding: utf-8 -*-
"""
@author = 'ethan'
"""
from django.urls import path

from qa.views import (UnansweredQuestionListView, AnsweredQuestionListView, CreateAnswerView,
                      CreateQuestionView, question_vote, accept_answer, answer_vote,
                      QuestionDetailView, QuestionListView)

app_name = "qa"

urlpatterns = [
    path('', UnansweredQuestionListView.as_view(), name='unanswered_q'),
    path('answered/', AnsweredQuestionListView.as_view(), name='answered_q'),
    path('indexed/', QuestionListView.as_view(), name='all_q'),
    path('ask-question/', CreateQuestionView.as_view(), name='ask_question'),
    path('question-detail/<int:pk>/', QuestionDetailView.as_view(), name='question_detail'),
    path('propose-answer/<int:question_id>/', CreateAnswerView.as_view(), name='propose_answer'),
    path('question/vote/', question_vote, name='question_vote'),
    path('answer/vote/', answer_vote, name='answer_vote'),
    path('accept-answer/', accept_answer, name='accept_answer'),
]
