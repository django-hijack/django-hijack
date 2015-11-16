from compat import url

from hijack import settings as hijack_settings
from hijack.views import release_hijack, disable_hijack_warning, login_with_id, login_with_email, login_with_username

urlpatterns = [
    url(r'^release-hijack/$', release_hijack, name='release_hijack')
]

if hijack_settings.HIJACK_DISPLAY_WARNING:
    urlpatterns.append(url(r'^disable-hijack-warning/$', disable_hijack_warning, name='disable_hijack_warning'))

hijacking_user_attributes = hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES
if 'email' in hijacking_user_attributes:
    urlpatterns.append(url(r'^email/(?P<email>[^@]+@[^@]+\.[^@]+)/$', login_with_email, name='login_with_email'))
if 'username' in hijacking_user_attributes:
    urlpatterns.append(url(r'^username/(?P<username>.*)/$', login_with_username, name='login_with_username'))
if 'user_id' in hijacking_user_attributes:
    urlpatterns.append(url(r'^(?P<user_id>[\w-]+)/$', login_with_id, name='login_with_id'))
