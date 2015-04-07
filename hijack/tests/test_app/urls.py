from compat import patterns, url

urlpatterns = patterns('hijack.tests.test_app.views', url(r'^$', 'hello',
                                                          name='hello'), )
