from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from hijack.contrib.admin import HijackUserAdminMixin

from . import models


@admin.register(models.CustomUser)
class CustomUserAdmin(UserAdmin):
    pass


@admin.register(models.Post)
class PostAdmin(HijackUserAdminMixin, admin.ModelAdmin):
    def get_hijack_user(self, obj):
        return obj.author
