from django.urls import reverse


class TestHijackUserAdminMixin:
    url = reverse("admin:test_app_customuser_changelist")

    def test_user_admin(self, admin_client):
        response = admin_client.get(self.url)
        assert response.status_code == 200
        assert (
            b'<button type="submit" class="button">hijack admin</button>'
            in response.content
        )
