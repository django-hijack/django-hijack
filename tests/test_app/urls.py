from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import views

app_name = "test_app"
urlpatterns = [
    path("hijack/", include("hijack.urls", namespace="hijack")),
    path("users/", views.UserListView.as_view(), name="user-list"),
    path("accounts/profile/", views.UserDetailView.as_view(), name="user-detail"),
    path(
        "bye-bye/", TemplateView.as_view(template_name="bye_bye.html"), name="bye-bye"
    ),
    path("admin/", admin.site.urls),
]
