from django.core.exceptions import ImproperlyConfigured
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth.admin import UserAdmin
from django.core.urlresolvers import reverse


class HijackUserAdminMixin(object):

    def hijack_field(self, obj):
        return '<a href="%s" class="button">Hijack %s</a>' % (reverse('hijack.views.login_with_id',args=(obj.id,)), obj)
    hijack_field.allow_tags = True
    hijack_field.short_description = 'Hijack User'


class HijackUserAdmin(HijackUserAdminMixin, UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',  'last_login', 'date_joined', 'is_staff', 'hijack_field',)
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email',)


# By default show a Hijack button in the admin panel for the User model.
if getattr(settings, "SHOW_HIJACKUSER_IN_ADMIN", True):
    default_user_model = 'auth.User'
    custom_user_model = getattr(settings, 'AUTH_USER_MODEL', default_user_model)
    if custom_user_model != default_user_model:
        raise ImproperlyConfigured(
            "`SHOW_HIJACKUSER_IN_ADMIN` does not work with a custom user"
            " model. Instead, mix in the `HijackUserAdminMixin` yourself")
    from django.contrib.auth.models import User

    admin.site.unregister(User)
    admin.site.register(User, HijackUserAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

if getattr(settings, "SHOW_SESSIONS_IN_ADMIN", False):
    admin.site.register(Session, SessionAdmin)
