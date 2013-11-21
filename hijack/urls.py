from django import VERSION as DJANGO_VERSION
if float("%d.%d"%(DJANGO_VERSION[0], DJANGO_VERSION[1])) <= 1.5:
    from django.conf.urls.defaults import patterns, url
else:    
    from django.conf.urls import patterns, url

 

urlpatterns = patterns('hijack.views',
    url(r'^email/(?P<email>[\w.%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,4})/$', 'login_with_email'),
    url(r'^username/(?P<username>\w+)/$', 'login_with_username'),
    url(r'^(?P<userId>\w+)/$', 'login_with_id'),
)
