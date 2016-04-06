from django.dispatch import Signal

post_superuser_login = Signal(providing_args=['user_id'])

post_superuser_logout = Signal(providing_args=['user_id'])

hijack_started = Signal(providing_args=['hijacker_id', 'hijacked_id'])
hijack_ended = Signal(providing_args=['hijacker_id', 'hijacked_id'])
