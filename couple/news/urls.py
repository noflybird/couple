from django.urls import path

from couple.news.views import (NewsListView, post_new, NewsDeleteView, like,
                               get_thread, post_comment, update_interactions)

app_name = "news"
urlpatterns = [
    path('', NewsListView.as_view(), name="list"),
    path('post-news/', post_new, name="post_news"),
    path('delete/<str:pk>', NewsDeleteView.as_view(), name="delete_news"),
    path('like/', like, name='like_post'),
    path('get-thread/', get_thread, name='get_thread'),
    path('post-comment/', post_comment, name='post_comments'),
    path('update-interactions/', update_interactions, name='update_interactions'),
]
