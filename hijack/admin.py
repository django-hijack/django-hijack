# -*- coding: utf-8 -*-
from compat import get_user_model
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse
from django.template.loader import get_template
from django.utils.translation import ugettext_lazy as _
from django import VERSION

from hijack import settings as hijack_settings

if VERSION < (1, 8):
    from django.template import Context


class HijackUserAdminMixin(object):
    def hijack_field(self, obj):
        hijack_attributes = hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES

        if 'user_id' in hijack_attributes:
            hijack_url = reverse('login_with_id', args=(obj.pk, ))
        elif 'email' in hijack_attributes:
            hijack_url = reverse('login_with_email', args=(obj.email, ))
        else:
            hijack_url = reverse('login_with_username', args=(obj.username, ))

        button_template = get_template(hijack_settings.HIJACK_BUTTON_TEMPLATE)
        button_context = {
            'hijack_url': hijack_url,
            'username': str(obj),
        }
        if VERSION < (1, 8):
            button_context = Context(button_context)

        return button_template.render(button_context)

    hijack_field.allow_tags = True
    hijack_field.short_description = _('Hijack user')


class HijackUserAdmin(HijackUserAdminMixin, UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',
                    'last_login', 'date_joined', 'is_staff', 'hijack_field', )
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email', )

# By default show a Hijack button in the admin panel for the User model.
if hijack_settings.HIJACK_DISPLAY_ADMIN_BUTTON:
    UserModel = get_user_model()
    admin.site.unregister(UserModel)
    admin.site.register(UserModel, HijackUserAdmin)
