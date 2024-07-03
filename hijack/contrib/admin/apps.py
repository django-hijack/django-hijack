import logging
import warnings

from django.apps import AppConfig
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)


class HijackAdminConfig(AppConfig):
    name = "hijack.contrib.admin"
    label = "hijack_admin"

    def ready(self):
        from django.contrib import admin

        from . import HijackUserAdminMixin

        UserModel = get_user_model()
        try:
            UserModelAdmin = type(admin.site._registry[UserModel])
        except KeyError:
            # User model may not be registered, see also:
            # https://github.com/django-hijack/django-hijack/issues/328
            warnings.warn(
                f"{UserModel.__qualname__} is not registered in the default admin."
                f" Please integrate hijack into your user admin manually.",
                UserWarning,
            )
        else:
            if issubclass(UserModelAdmin, HijackUserAdminMixin):
                logger.debug(
                    "UserModelAdmin already is a subclass of HijackUserAdminMixin."
                )
            else:
                admin.site.unregister(UserModel)

                # We create a subclass including the HijackUserAdminMixin but keep
                # the name and module, to keep output form failing checks consistent.
                HijackUserModelAdmin = type(
                    UserModelAdmin.__name__, (HijackUserAdminMixin, UserModelAdmin), {}
                )
                HijackUserModelAdmin.__module__ = UserModelAdmin.__module__

                admin.site.register(UserModel, HijackUserModelAdmin)
