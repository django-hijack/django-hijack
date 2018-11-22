from django.dispatch import Signal

hijack_started = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request', 'hijacker', 'hijacked', 'pre_hijack_started_results'])
hijack_ended = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request', 'hijacker', 'hijacked', 'pre_hijack_ended_results'])

pre_hijack_started = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request', 'hijacker', 'hijacked'])
pre_hijack_ended = Signal(providing_args=['hijacker_id', 'hijacked_id', 'request', 'hijacker', 'hijacked'])
