"""URLs to run the tests."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('hijack/', include('hijack.urls', namespace='hijack')),
    path('hello/', include('hijack.tests.test_app.urls', 'test_app')),
]
