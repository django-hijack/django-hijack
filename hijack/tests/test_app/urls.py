from compat import url
from django.views.generic import TemplateView

app_name = 'test_app'
urlpatterns = [
    url(r'^filter/$', TemplateView.as_view(template_name='hello_filter.html'), name='hello_filter'),
    url(r'^$', TemplateView.as_view(template_name='hello.html'), name='hello'),
]
