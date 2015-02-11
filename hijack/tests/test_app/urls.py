from compat import patterns, url

from . import views
 
urlpatterns = patterns('hijack.tests.test_app.views',
    url(r'^$', 'hello', name='hello'),
    
)
