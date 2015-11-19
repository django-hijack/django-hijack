
from hijack.helpers import is_authorized_default


def can_hijack_default(hijacker, hijacked):
    return is_authorized_default(hijacker, hijacked)


def everybody_can_hijack(hijacker, hijacked):
    return True


def nobody_can_hijack(hijacker, hijacked):
    return False
