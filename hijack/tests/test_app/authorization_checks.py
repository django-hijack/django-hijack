
from hijack.helpers import is_authorized


def can_hijack_default(hijacker, hijacked):
    return is_authorized(hijacker, hijacked)


def everybody_can_hijack(hijacker, hijacked):
    return True


def nobody_can_hijack(hijacker, hijacked):
    return False
