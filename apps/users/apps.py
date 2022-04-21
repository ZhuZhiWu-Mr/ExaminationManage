from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'apps.users'
    default_auto_field = "django.db.models.BigAutoField"
    verbose_name = "用户"