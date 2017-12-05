from compat import url

from hijack import settings as hijack_settings
from hijack import views

app_name = 'hijack'
urlpatterns = [
    url(
        r'^release-hijack/$',
        views.release_hijack,
        name='release_hijack'
    )
]

if hijack_settings.HIJACK_DISPLAY_WARNING:
    urlpatterns.append(url(
        r'^disable-hijack-warning/$',
        views.disable_hijack_warning,
        name='disable_hijack_warning'
    ))

hijacking_user_attributes = hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES
if 'email' in hijacking_user_attributes:
    urlpatterns.append(url(
        r'^email/(?P<email>[^@\s]+@[^@\s]+\.[^@\s]+)/$',
        views.login_with_email,
        name='login_with_email'
    ))
if 'username' in hijacking_user_attributes:
    urlpatterns.append(url(
        r'^username/(?P<username>.*)/$',
        views.login_with_username,
        name='login_with_username'
    ))
if 'user_id' in hijacking_user_attributes:
    urlpatterns.append(url(
        r'^(?P<user_id>[\w-]+)/$',
        views.login_with_id,
        name='login_with_id'
    ))
