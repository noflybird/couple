from __future__ import unicode_literals
import uuid
from collections import Counter

from six import python_2_unicode_compatible
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericRelation, GenericForeignKey
from django.db import models

from slugify import slugify
from markdownx.models import MarkdownxField
from taggit.managers import TaggableManager
from markdownx.utils import markdownify


@python_2_unicode_compatible
class Vote(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='qa_vote',
                             on_delete=models.CASCADE, verbose_name='用户')
    value = models.BooleanField(default=True, verbose_name='赞同或反对')
    content_type = models.ForeignKey(ContentType, related_name='votes_on', on_delete=models.CASCADE)
    object_id = models.CharField(max_length=255)
    vote = GenericForeignKey('content_type', 'object_id')

    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '投票'
        verbose_name_plural = verbose_name
        unique_together = ('user', 'content_type', 'object_id')
        index_together = ('content_type', 'object_id')


@python_2_unicode_compatible
class QuestionQuerySet(models.query.QuerySet):

    def get_answered(self):
        """已有答案的问题"""
        return self.filter(has_answer=True).select_related('user')

    def get_unanswered(self):
        """未被的回答的问题"""
        return self.filter(has_answer=False).select_related('user')

    def get_counted_tags(self):
        """统计所有问题标签的数量(大于0的)"""
        tag_dict = {}
        for obj in self.all():
            for tag in obj.tags.names():
                if tag not in tag_dict:
                    tag_dict[tag] = 1

                else:
                    tag_dict[tag] += 1
        return tag_dict.items()


@python_2_unicode_compatible
class Question(models.Model):
    STATUS = (("O", "Open"), ("C", "Close"), ("D", "Draft"))

    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="q_author",
                             on_delete=models.CASCADE, verbose_name='提问者')
    title = models.CharField(max_length=255, unique=True, verbose_name='标题')
    slug = models.SlugField(max_length=80, null=True, blank=True, verbose_name='(URL)别名')
    status = models.CharField(max_length=1, choices=STATUS, default='O',
                              verbose_name='问题状态')
    content = MarkdownxField(verbose_name='内容')
    tags = TaggableManager(help_text='多个标签使用,(英文)隔开', verbose_name='标签')
    has_answer = models.BooleanField(default=False, verbose_name="接受回答")
    votes = GenericRelation(Vote, verbose_name='投票情况')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    objects = QuestionQuerySet.as_manager()

    class Meta:
        verbose_name = '问题'
        verbose_name_plural = verbose_name
        ordering = ("-created_at",)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Question, self).save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数"""
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]

    def get_answers(self):
        """获取所有的回答"""
        return Answer.objects.filter(question=self).select_related('user', 'question')

    def count_answers(self):
        """回答的数量"""
        return self.get_answers().count()

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True).select_related('user').prefecth_related('vote')]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False).select_related('user').prefecth_related('vote')]


@python_2_unicode_compatible
class Answer(models.Model):
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='a_author', on_delete=models.CASCADE,
                             verbose_name='回答者')
    question = models.ForeignKey(Question, on_delete=models.CASCADE, verbose_name='问题')
    content = MarkdownxField(verbose_name='内容')
    is_answer = models.BooleanField(default=False, verbose_name='回答是否被接受')
    votes = GenericRelation(Vote, verbose_name='投票情况')
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        ordering = ('-is_answer', '-created_at')
        verbose_name = '回答'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.content

    def get_markdown(self):
        return markdownify(self.content)

    def total_votes(self):
        """得票数"""
        dic = Counter(self.votes.values_list('value', flat=True))
        return dic[True] - dic[False]

    def get_upvoters(self):
        """赞同的用户"""
        return [vote.user for vote in self.votes.filter(value=True).select_related('user').prefecth_related('vote')]

    def get_downvoters(self):
        """反对的用户"""
        return [vote.user for vote in self.votes.filter(value=False).select_related('user').prefecth_related('vote')]

    def accept_answer(self):
        """接受回答"""
        answer_set = Answer.objects.filter(question=self.question)
        answer_set.update(is_answer=False)
        self.is_answer = True
        self.save()
        self.question.has_answer = True
        self.question.save()
