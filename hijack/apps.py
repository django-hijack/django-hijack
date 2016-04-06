# -*- coding: utf-8 -*-
from django.apps import AppConfig


class HijackConfig(AppConfig):
    name = 'hijack'
    verbose_name = 'Hijack'

    def ready(self):
        from hijack.checks import register_checks
        register_checks()
