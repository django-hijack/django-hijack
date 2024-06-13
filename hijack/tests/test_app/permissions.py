def allow_all(*, hijacker, hijacked):
    return True


def deny_all(*, hijacker, hijacked):
    return False


def require_request_required(*, hijacker, hijacked, request):
    return True


def require_request_optional(*, hijacker, hijacked, request=None):
    return True
