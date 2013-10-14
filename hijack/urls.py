"""URLs for the hijack app."""
from django.conf.urls.defaults import patterns, url

# from . import views

urlpatterns = patterns('hijack.views', 
    url(r'^(?P<userID>\w+)', 'login_as'),
)
