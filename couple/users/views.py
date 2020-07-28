from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views.generic import DetailView, UpdateView

User = get_user_model()


class UserDetailView(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'users/user_detail.html'
    slug_field = 'username'
    slug_url_kwarg = 'username'

    def get_context_data(self, **kwargs):
        context = super(UserDetailView, self).get_context_data(**kwargs)
        user = User.objects.get(username=self.request.user.username)
        context["moments_num"] = user.publisher.filter(reply=False).count()
        context["article_num"] = user.author.filter(status='P').count()  # 只算已发表的文章
        context["comment_num"] = user.publisher.filter(
            reply=True).count() + user.comment_comments.all().count()  # 文章+动态的评论数
        context["question_num"] = user.q_author.all().count()
        context["answer_num"] = user.a_author.all().count()
        tmp = set()
        sent_num = user.sent_messages.all()
        for i in sent_num:
            tmp.add(i.recipient.username)
        received_num = user.received_messages.all()
        for r in received_num:
            tmp.add(r.sender.username)

        context["interaction_num"] = user.liked_news.all().count() + user.qa_vote.all().count() + context[
            "comment_num"] + len(tmp)
        return context


user_detail_view = UserDetailView.as_view()


class UserUpdateView(LoginRequiredMixin, UpdateView):

    model = User
    template_name = "users/user_form.html"
    fields = ['nickname', 'email', 'picture', 'introduction', 'job_title', 'location',
              'personal_url', 'weibo', 'zhihu', 'github', 'linkedin']

    def get_success_url(self):
        return reverse('users:detail', kwargs={'username': self.request.user.username})

    def get_object(self, queryset=None):
        return self.request.user


user_update_view = UserUpdateView.as_view()
