
from hijack.helpers import is_authorized


def can_hijack_default(hijacker, hijacked):
    return is_authorized(hijacker, hijacked)


def can_hijack_yes(hijacker, hijacked):
    return True


def can_hijack_no(hijacker, hijacked):
    return False
