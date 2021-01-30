from django.views.generic import TemplateView
from django.urls import path

app_name = 'test_app'
urlpatterns = [
    path('filter/', TemplateView.as_view(template_name='hello_filter.html'), name='hello_filter'),
    path('', TemplateView.as_view(template_name='hello.html'), name='hello'),
]
