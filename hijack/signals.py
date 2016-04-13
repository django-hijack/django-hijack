from django.dispatch import Signal

hijack_started = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request'])
hijack_ended = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request'])

# Deprecated signals
post_superuser_login = Signal(providing_args=['user_id'])
post_superuser_logout = Signal(providing_args=['user_id'])
