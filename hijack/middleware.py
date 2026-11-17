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
        user = request.user
        request.user = SimpleLazyObject(
            lambda: self.setup_user(request, copy.copy(user))
        )
        if "REMOTE_USER" in request.META and request.user.is_hijacked:
            request.META["REMOTE_USER"] = request.user.get_username()

    def process_response(self, request, response):
        """Render hijack notification and inject into HTML response."""
        session = request.session
        insert_before = settings.HIJACK_INSERT_BEFORE
        content_encoding = response.get("Content-Encoding", "")
        content_type = response.get("Content-Type", "").split(";")[0]

        has_insertion_point = insert_before is not None
        session_was_accessed = session.accessed
        has_session_data = not session.is_empty()
        is_html = (
            not getattr(response, "streaming", False)
            and not content_encoding
            and content_type in _HTML_TYPES
        )
        # Reading the session sets `accessed` and adds a `Vary: Cookie` header.
        # Do not do that for a session the view never used.
        is_hijacked = session_was_accessed and bool(session.get("hijack_history"))
        if has_insertion_point and has_session_data and is_html and is_hijacked:
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
