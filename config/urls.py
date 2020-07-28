from django.conf import settings
from django.conf.urls.static import static

from django.urls import include, path
from django.views import defaults as default_views
import xadmin

from couple.news.views import NewsListView

urlpatterns = [
    # path("", TemplateView.as_view(template_name="pages/home.html"), name="home"),
    # path(
    #     "about/", TemplateView.as_view(template_name="pages/about.html"), name="about"
    # ),
    # Django Admin, use {% url 'admin:index' %}
    # path(settings.ADMIN_URL, admin.site.urls),
    # User management
    path("markdownx/", include('markdownx.urls')),
    path('comments/', include('django_comments.urls')),
    path('admin/', xadmin.site.urls),

    path('', NewsListView.as_view(), name='home'),
    path('users/', include('couple.users.urls', namespace='users')),
    path("accounts/", include("allauth.urls")),
    # Your stuff: custom urls includes go here
    path("news/", include('couple.news.urls', namespace='news')),
    path("articles/", include('couple.articles.urls', namespace='articles')),
    path("qa/", include('couple.qa.urls', namespace='qa')),
    path("messager/", include('couple.messager.urls', namespace='messages')),
    path("notifications/", include('couple.notifications.urls', namespace='notifications')),
    path("search/", include('haystack.urls'))
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "403/",
            default_views.permission_denied,
            kwargs={"exception": Exception("Permission Denied")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
    ]
    if "debug_toolbar" in settings.INSTALLED_APPS:
        import debug_toolbar

        urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
