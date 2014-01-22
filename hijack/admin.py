from django.contrib.auth.models import User
from django.contrib import admin
from django.contrib.sessions.models import Session
from django.conf import settings
from django.contrib.auth.admin import UserAdmin


 



class HijackUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',  'last_login', 'date_joined', 'is_staff', 'hijack_field',)
    list_filter = ('is_staff', 'is_superuser')
    search_fields = ('username', 'first_name', 'last_name', 'email',)

    def hijack_field(self, obj):
        return '<a href="/hijack/%s" class="button">Hijack %s</a>' % (str(obj.id), obj.username)
    hijack_field.allow_tags = True
    hijack_field.short_description = 'Hijack User'

admin.site.unregister(User)
admin.site.register(User, HijackUserAdmin)


class SessionAdmin(admin.ModelAdmin):
    def _session_data(self, obj):
        return obj.get_decoded()
    list_display = ['session_key', '_session_data', 'expire_date']

if getattr(settings, "SHOW_SESSIONS_IN_ADMIN", False):
    admin.site.register(Session, SessionAdmin)
