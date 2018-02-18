from django.dispatch import Signal

hijack_started = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request', 'hijacker', 'hijacked'])
hijack_ended = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request', 'hijacker', 'hijacked'])

