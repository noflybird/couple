from django.urls import path
from users.views import UserDetailView, UserUpdateView

app_name = "users"
urlpatterns = [
    path("update/", UserDetailView.as_view(), name="update"),
    path("<str:username>/", UserUpdateView.as_view(), name="detail"),
]
