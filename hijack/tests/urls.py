"""URLs to run the tests."""
from compat import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^hijack/', include('hijack.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^hello$', include('hijack.tests.test_app.urls'))
)
