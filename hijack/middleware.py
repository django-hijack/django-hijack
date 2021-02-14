import re

from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin

from hijack import settings

_HTML_TYPES = ("text/html", "application/xhtml+xml")


class HijackRemoteUserMiddleware(MiddlewareMixin):
    """
    Middleware for hijack RemoteUser.

    One must place this middleware between
    'django.contrib.auth.middleware.AuthenticationMiddleware' and
    'django.contrib.auth.middleware.RemoteUserMiddleware' in MIDDLEWARE_CLASSES

    Just makes remote user same as hijacked
    """

    header = "REMOTE_USER"

    def process_request(self, request):
        is_hijacked = request.session.get("is_hijacked_user", False)
        remote_username = request.META.get(self.header, None)
        if not is_hijacked or not remote_username:
            return
        # Ok, we hijacked and remote. Just assign hijacked user to remote
        if callable(request.user.is_authenticated):
            is_authenticated = request.user.is_authenticated()
        else:
            is_authenticated = request.user.is_authenticated
        if is_authenticated:
            username = request.user.get_username()
            if username != remote_username:
                request.META[self.header] = username

    def process_response(self, request, response):
        if not request.session.get("is_hijacked_user"):
            return response

        # Check for responses where the toolbar can't be inserted.
        content_encoding = response.get("Content-Encoding", "")
        content_type = response.get("Content-Type", "").split(";")[0]
        if (
            getattr(response, "streaming", False)
            or "gzip" in content_encoding
            or content_type not in _HTML_TYPES
        ):
            return response

        rendered = render_to_string(
            "hijack/snackbar.html",
            {"request": request, "csrf_token": request.META["CSRF_COOKIE"]},
        )

        # Insert the toolbar in the response.
        content = response.content.decode(response.charset)
        insert_before = settings.HIJACK_INSERT_BEFORE
        pattern = re.escape(insert_before)
        bits = re.split(pattern, content, flags=re.IGNORECASE)
        if len(bits) > 1:
            bits[-2] += rendered
            response.content = insert_before.join(bits)
            if "Content-Length" in response:
                response["Content-Length"] = len(response.content)
        return response
