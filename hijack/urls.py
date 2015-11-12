from compat import patterns, url

from hijack import settings as hijack_settings


urlpatterns = patterns('hijack.views',
                       url(r'^release-hijack/$', 'release_hijack',
                           name='release_hijack'), )

if hijack_settings.HIJACK_DISPLAY_WARNING:
    urlpatterns += patterns('hijack.views',
                            url(r'^disable-hijack-warning/$',
                                view='disable_hijack_warning',
                                name='disable_hijack_warning', ), )

hijacking_user_attributes = hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES

if 'email' in hijacking_user_attributes:
    urlpatterns += patterns('hijack.views',
                            url(r'^email/(?P<email>[^@]+@[^@]+\.[^@]+)/$',
                                view='login_with_email',
                                name='login_with_email', ), )
if 'username' in hijacking_user_attributes:
    urlpatterns += patterns('hijack.views',
                            url(r'^username/(?P<username>.*)/$',
                                view='login_with_username',
                                name='login_with_username', ), )
if 'user_id' in hijacking_user_attributes:
    urlpatterns += patterns('hijack.views', url(r'^(?P<user_id>[\w-]+)/$',
                                                view='login_with_id',
                                                name='login_with_id', ), )
