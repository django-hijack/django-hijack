
from hijack.helpers import can_hijack


def can_hijack_default(hijacker, hijacked):
    return can_hijack(hijacker, hijacked)


def can_hijack_yes(hijacker, hijacked):
    return True


def can_hijack_no(hijacker, hijacked):
    return False
