class HijackRemoteUserMiddleware(object):
    """
    Middleware for hijack RemoteUser. One must place this middleware between
    'django.contrib.auth.middleware.AuthenticationMiddleware' and
    'django.contrib.auth.middleware.RemoteUserMiddleware' in MIDDLEWARE_CLASSES

    Just makes remote user same as hijacked
    """
    header = "REMOTE_USER"

    def process_request(self, request):
        is_hijacked = request.session.get('is_hijacked_user', False)
        remote_username = request.META.get(self.header, None)
        if not is_hijacked or not remote_username:
            return
        # Ok, we hijacked and remote. Just assign hijacked user to remote
        if request.user.is_authenticated():
            username = request.user.get_username()
            if username != remote_username:
                request.META[self.header] = username
                
    def authenticate(self, *args, **kwargs):
        return None
