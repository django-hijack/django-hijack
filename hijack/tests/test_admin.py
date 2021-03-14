from django.urls import reverse

from hijack.tests.test_app.models import Post


class TestHijackUserAdminMixin:
    def test_user_admin(self, admin_client):
        url = reverse("admin:test_app_customuser_changelist")
        response = admin_client.get(url)
        assert response.status_code == 200
        assert (
            b'<button type="submit" class="button">HIJACK</button>' in response.content
        )

    def test_related_user(self, admin_client, admin_user):
        url = reverse("admin:test_app_post_changelist")
        Post.objects.create(author=admin_user)
        response = admin_client.get(url)
        assert response.status_code == 200
        assert b"Hijack admin" in response.content
