from compat import patterns, url
from django.conf import settings

urlpatterns = patterns('hijack.views',
    url(r'^release-hijack/$', 'release_hijack', name='release_hijack'),
)

if getattr(settings, "HIJACK_NOTIFY_ADMIN", False):
    urlpatterns += patterns('hijack.views',
        url(r'^disable-hijack-warning/$', 'disable_hijack_warning', name='disable_hijack_warning'),
)

hijacking_user_attributes = getattr(settings, "ALLOWED_HIJACKING_USER_ATTRIBUTES", False)

if not hijacking_user_attributes or 'email' in hijacking_user_attributes:
    urlpatterns += patterns('hijack.views',
        url(r'^email/(?P<email>[^@]+@[^@]+\.[^@]+)/$', 'login_with_email', name='login_with_email')
    )
if not hijacking_user_attributes or 'username' in hijacking_user_attributes:
    urlpatterns += patterns('hijack.views',
        url(r'^username/(?P<username>\w+)/$', 'login_with_username', name='login_with_username'),
    )
if not hijacking_user_attributes or 'user_id' in hijacking_user_attributes:
    urlpatterns += patterns('hijack.views',
        url(r'^(?P<user_id>\w+)/$', 'login_with_id', name='login_with_id')
    )
