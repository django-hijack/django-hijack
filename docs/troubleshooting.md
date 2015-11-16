
# Why does the hijack button not show up in the admin site?
If your ``UserAdmin`` object is already registered in the admin site through another app, you can disable the registration by Django Hijack setting ``HIJACK_DISPLAY_ADMIN_BUTTON = False`` in your project settings.

Afterwards, create a new ``UserAdmin`` class derived from ``HijackUserAdmin``. Example:

```python
from django.contrib import admin
from custom_app.admin import MyCustomUserAdmin
from custom_app.models import MyCustomUser

from hijack.admin import HijackUserAdminMixin

admin.site.unregister(MyCustomUser)


class MyCustomUserAdminWithHijackButton(HijackUserAdminMixin, MyCustomUserAdmin):
    """
    We are subclassing HijackUserAdminMixin to display the hijack button in the admin.
    """
    list_display = MyCustomUserAdmin.list_display + ('hijack_field', )

admin.site.register(MyCustomUser, MyCustomUserAdminWithHijackButton)
```

    
# I do not see a notification bar when hijacking another user
* Follow the steps described in "Setting up the notification bar" in the installation settings.
* `HIJACK_DISPLAY_WARNING` must not be set to False in your project settings (default: True).
* Make sure that `django.template.context_processors.request` is in your template context processors.
* Make sure that ``django.contrib.staticfiles`` is included in your ``INSTALLED_APPS``, and do not forget to run ``python manage.py collectstatic``.