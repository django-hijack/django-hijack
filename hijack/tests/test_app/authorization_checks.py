from hijack.permissions import has_hijack_perm


def can_hijack_default(hijacker, hijacked):
    return has_hijack_perm(hijacker, hijacked)


def everybody_can_hijack(hijacker, hijacked):
    return True


def nobody_can_hijack(hijacker, hijacked):
    return False
