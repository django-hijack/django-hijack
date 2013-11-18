"""URLs for the hijack app."""
from django.conf.urls.defaults import patterns, url

# from . import views

urlpatterns = patterns('hijack.views',
    url(r'^email/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 'login_with_email'),
    url(r'^username/(?P<username>\w+)/$', 'login_with_username'),
    url(r'^(?P<userId>\w+)/$', 'login_with_id'),
)
