import copy
import re

from django.template.loader import render_to_string
from django.utils.deprecation import MiddlewareMixin
from django.utils.functional import SimpleLazyObject

from hijack.conf import settings

__all__ = ["HijackUserMiddleware"]

_HTML_TYPES = ("text/html", "application/xhtml+xml")


class HijackUserMiddleware(MiddlewareMixin):
    """Set `is_hijacked` attribute; render and inject notification."""

    @staticmethod
    def setup_user(request, user):
        """Set `is_hijacked` attribute."""
        user.is_hijacked = bool(request.session.get("hijack_history", []))
        return user

    def process_request(self, request):
        """Set `is_hijacked` and override REMOTE_USER header."""
        user = copy.copy(request.user)  # prevent recursion error
        request.user = SimpleLazyObject(lambda: self.setup_user(request, user))
        if "REMOTE_USER" in request.META and request.user.is_hijacked:
            request.META["REMOTE_USER"] = request.user.get_username()

    def process_response(self, request, response):
        """Render hijack notification and inject into HTML response."""
        if request.session.is_empty() or not request.session.accessed:
            # do not touch empty sessions to avoid unnecessary vary on cookie header
            return response

        insert_before = settings.HIJACK_INSERT_BEFORE
        if not getattr(request.user, "is_hijacked", False) or insert_before is None:
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
            "hijack/notification.html",
            {"request": request},
            request=request,
        )

        # Insert the toolbar in the response.
        content = response.content.decode(response.charset)
        pattern = re.escape(insert_before)
        bits = re.split(pattern, content, flags=re.IGNORECASE)
        if len(bits) > 1:
            bits[-2] += rendered
            response.content = insert_before.join(bits)
            if "Content-Length" in response:
                response["Content-Length"] = len(response.content)
        return response
