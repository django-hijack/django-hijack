from django.apps import AppConfig
from django.contrib.auth import get_user_model


class HijackAdminConfig(AppConfig):
    name = "hijack.contrib.admin"
    label = "hijack admin"

    def ready(self):
        from django.contrib import admin

        from . import HijackUserAdminMixin

        UserModel = get_user_model()
        UserModelAdmin = type(admin.site._registry[UserModel])
        admin.site.unregister(UserModel)

        HijackUserModelAdmin = type(
            UserModelAdmin.__name__, (HijackUserAdminMixin, UserModelAdmin), {}
        )
        HijackUserModelAdmin.__module__ = UserModelAdmin.__module__

        admin.site.register(UserModel, HijackUserModelAdmin)
