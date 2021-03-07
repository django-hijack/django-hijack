from unittest.mock import MagicMock

from django.contrib.auth import get_user_model
from django.http import HttpResponse, JsonResponse

from hijack import middleware


class TestHijackRemoteUserMiddleware:
    middleware = middleware.HijackUserMiddleware(lambda x: None)

    def test_process_request__hijacked(self, rf, bob, alice):
        request = rf.get("/")
        request.user = bob
        request.session = {"hijack_history": [str(alice.pk)]}
        self.middleware.process_request(request)
        assert bob.is_hijacked

    def test_process_request__not_hijacked(self, rf, bob):
        request = rf.get("/")
        request.user = bob
        request.session = {}
        self.middleware.process_request(request)
        assert not bob.is_hijacked

    def test_process_request__remote_user__hijacked(self, rf, bob, alice):
        request = rf.get("/")
        request.user = bob
        request.META["REMOTE_USER"] = "eve"
        request.session = {"hijack_history": [str(alice.pk)]}
        self.middleware.process_request(request)
        assert bob.is_hijacked
        assert request.META["REMOTE_USER"] == "bob"

    def test_process_request__remote_user__not_hijacked(self, rf, bob):
        request = rf.get("/")
        request.user = bob
        request.META["REMOTE_USER"] = "eve"
        request.session = {}
        self.middleware.process_request(request)
        assert not bob.is_hijacked
        assert request.META["REMOTE_USER"] == "eve"

    def test_process_response__html(self, rf, monkeypatch):
        request = rf.get("/")
        request.user = get_user_model()
        request.user.is_hijacked = True
        request.META["CSRF_COOKIE"] = "123456"
        render_to_string = MagicMock()
        response = HttpResponse("")
        monkeypatch.setattr("hijack.middleware.render_to_string", render_to_string)
        assert self.middleware.process_response(request, response) is response
        render_to_string.assert_called_once_with(
            "hijack/notification.html",
            {"request": request, "csrf_token": "123456"},
        )

    def test_process_response__non_html(self, rf, monkeypatch):
        request = rf.get("/")
        request.user = get_user_model()
        request.user.is_hijacked = True
        render_to_string = MagicMock()
        response = JsonResponse({})
        monkeypatch.setattr("hijack.middleware.render_to_string", render_to_string)
        assert self.middleware.process_response(request, response) is response
        render_to_string.assert_not_called()

    def test_process_response__content_length(self, rf, monkeypatch):
        request = rf.get("/")
        request.user = get_user_model()
        request.user.is_hijacked = True
        request.META["CSRF_COOKIE"] = "123456"
        render_to_string = MagicMock()
        render_to_string.return_value = "HIJACKED"
        response = HttpResponse(b"<body></body>")
        response["Content-Length"] = "13"
        monkeypatch.setattr("hijack.middleware.render_to_string", render_to_string)
        assert self.middleware.process_response(request, response) is response
        render_to_string.assert_called_once_with(
            "hijack/notification.html",
            {"request": request, "csrf_token": "123456"},
        )
        assert response["Content-Length"] == "21"
        assert response.content == b"<body>HIJACKED</body>"
