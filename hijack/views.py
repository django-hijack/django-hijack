import django
from django.contrib.auth import BACKEND_SESSION_KEY, get_user_model, load_backend, login
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.module_loading import import_string
from django.views import View
from django.views.decorators.csrf import csrf_protect
from django.views.generic.detail import SingleObjectMixin

if django.VERSION >= (3, 0):
    from django.utils.http import url_has_allowed_host_and_scheme
else:
    from django.utils.http import is_safe_url as url_has_allowed_host_and_scheme

from hijack import signals
from hijack.conf import settings


def get_used_backend(request):
    backend_str = request.session[BACKEND_SESSION_KEY]
    backend = load_backend(backend_str)
    return backend


class SuccessUrlMixin:
    redirect_field_name = "next"

    success_url = "/"

    def get_success_url(self):
        url = self.get_redirect_url()
        return url or self.success_url

    def get_redirect_url(self):
        """Return the user-originating redirect URL if it's safe."""
        redirect_to = self.request.POST.get(
            self.redirect_field_name, self.request.GET.get(self.redirect_field_name, "")
        )
        url_is_safe = url_has_allowed_host_and_scheme(
            url=redirect_to,
            allowed_hosts=self.request.get_host(),
            require_https=self.request.is_secure(),
        )
        return redirect_to if url_is_safe else ""


class AcquireUserView(
    LoginRequiredMixin, UserPassesTestMixin, SuccessUrlMixin, SingleObjectMixin, View
):
    model = get_user_model()
    success_url = settings.LOGIN_REDIRECT_URL

    def test_func(self):
        func = import_string(settings.HIJACK_PERMISSION_CHECK)
        return func(hijacker=self.request.user, hijacked=self.get_object())

    def get_object(self, queryset=None):
        return get_object_or_404(self.model, pk=self.request.POST["user_pk"])

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        hijacker = request.user
        hijacked = self.get_object()

        hijack_history = request.session.get("hijack_history", [])
        hijack_history.append(request.user._meta.pk.value_to_string(hijacker))

        backend = get_used_backend(request)
        backend = f"{backend.__module__}.{backend.__class__.__qualname__}"

        with signals.no_update_last_login():
            login(request, hijacked, backend=backend)

        request.session["hijack_history"] = hijack_history

        signals.hijack_started.send(
            sender=None,
            request=request,
            hijacker=hijacker,
            hijacked=hijacked,
        )
        return HttpResponseRedirect(self.get_success_url())


acquire_user_view = AcquireUserView.as_view()


class ReleaseUserView(LoginRequiredMixin, SuccessUrlMixin, View):

    success_url = settings.LOGOUT_REDIRECT_URL

    @method_decorator(csrf_protect)
    def post(self, request, *args, **kwargs):
        hijack_history = request.session.get("hijack_history", [])

        if not hijack_history:
            raise Http404

        hijacked = request.user
        user_pk = hijack_history.pop()
        hijacker = get_object_or_404(get_user_model(), pk=user_pk)
        backend = get_used_backend(request)
        backend = f"{backend.__module__}.{backend.__class__.__qualname__}"
        with signals.no_update_last_login():
            login(request, hijacker, backend=backend)

        request.session["hijack_history"] = hijack_history

        signals.hijack_ended.send(
            sender=None,
            request=request,
            hijacker=hijacker,
            hijacked=hijacked,
        )
        return HttpResponseRedirect(self.get_success_url())


release_user_view = ReleaseUserView.as_view()
