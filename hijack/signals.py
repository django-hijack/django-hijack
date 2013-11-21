from django.dispatch import Signal

post_superuser_login = Signal(providing_args=['user_id'])

post_superuser_logout = Signal(providing_args=['user_id'])