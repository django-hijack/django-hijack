from appconf import AppConf
from django.conf import settings

__all__ = ["settings"]


class HijackConf(AppConf):
    PERMISSION_CHECK = "hijack.permissions.superusers_only"
    INSERT_BEFORE = "</body>"

    class Meta:
        prefix = "hijack"
