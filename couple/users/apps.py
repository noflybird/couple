from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class UsersConfig(AppConfig):
    name = "couple.users"
    verbose_name = "用户"

    def ready(self):
        try:
            import couple.users.signals  # noqa F401
        except ImportError:
            pass
