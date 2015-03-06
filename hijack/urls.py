from compat import patterns, url
from django.conf import settings

urlpatterns = patterns('hijack.views',
    url(r'^release-hijack/$', 'release_hijack', name='release_hijack'),
    url(r'^email/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 'login_with_email', name='login_with_email'),
    url(r'^username/(?P<username>\w+)/$', 'login_with_username', name='login_with_username'),
    url(r'^(?P<userId>\w+)/$', 'login_with_id', name='login_with_id'),
)

if getattr(settings, "HIJACK_NOTIFY_ADMIN", False):
    urlpatterns += patterns('hijack.views',
        url(r'^disable-hijack-warning/$', 'disable_hijack_warning', name='disable_hijack_warning'),
    )
