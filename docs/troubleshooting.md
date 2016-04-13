
# I do not see a notification bar when hijacking another user
* Make sure that you have followed the steps described in "Setting up the notification bar" in the installation settings.
* `HIJACK_DISPLAY_WARNING` must not be set to `False` in your project settings (default: `True`).
* Make sure that `django.template.context_processors.request` is in your template context processors.
* Make sure that ``django.contrib.staticfiles`` is included in your ``INSTALLED_APPS``, and do not forget to run ``python manage.py collectstatic``.
