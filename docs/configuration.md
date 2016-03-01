
# Notification bar
The template used for the notification bar is named "hijack/notifications.html", or "hijack/notifications_bootstrap.html" 
if Bootstrap is enabled.

## Bootstrap
If your project uses Bootstrap, you may want to set `HIJACK_USE_BOOTSTRAP = True` in your project settings.
Django Hijack will use a Bootstrap notification bar that does not overlap with the default navbar.

## Disabling the notification bar
You can temporarily disable the notification bar by setting `HIJACK_DISPLAY_WARNING = False`. 

# Permissions
By default, only superusers are allowed to hijack other users.
Django Hijack gives you a variety of options to extend the group of authorized users.

## Staff members
Set `HIJACK_AUTHORIZE_STAFF = True` in your project settings to authorize staff members to hijack non-staff users.
If you want staff to be able to hijack other staff as well, enable `HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF`.

Note that there is no option to authorize staff members to hijack superusers as this would undermine the distinction between staff users and superusers.

## Custom authorization function
Advanced Django developers might want to define their own check whether a user may hijack another user. This can be achieved by 
setting `HIJACK_AUTHORIZATION_CHECK` to the dotted path of a function which accepts two User 
objects – `hijacker` and `hijacked` – and returns a Boolean value. Example:

```python
# settings.py
HIJACK_AUTHORIZATION_CHECK = 'mysite.utils.my_authorization_check'
```

```python
# mysite.utils.py
def my_authorization_check(hijacker, hijacked):
    """
    Checks if a user is authorized to hijack another user
    """
    if my_condition:
        return True
    else:
        return False
```

**Warning: The setting `HIJACK_AUTHORIZATION_CHECK` overrides the other hijack authorization settings. Defining a custom authorization function can have dangerous
effects on your application's authorization system. Potentially, it might allow any user to impersonate 
any other user and to take advantage of all their permissions.**

## Custom view decorator
Django Hijack's views are decorated by Django's `staff_member_required` decorator. If you have written your own 
authorization function, or haven't installed `django.contrib.admin`, you may want to override this behaviour by 
setting `HIJACK_DECORATOR` to the dotted path of a custom decorator. Example:

```python
HIJACK_DECORATOR = 'mysite.decorators.mydecorator'
```

# Remote users
To work with `REMOTE_USER`,  place `'hijack.middleware.HijackRemoteUserMiddleware'`
between `'django.contrib.auth.middleware.AuthenticationMiddleware'` and `'django.contrib.auth.middleware.RemoteUserMiddleware'`:

```python
# settings.py
MIDDLEWARE_CLASSES = (
    ...,
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hijack.middleware.HijackRemoteUserMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    ...,
)
```

# Custom user models
Django Hijack supports custom user models. Just modify your custom UserAdmin class as shown in this example:

```python
# mysite/admin.py
from hijack.admin import HijackUserAdminMixin

class MyCustomUserAdmin(UserAdmin, HijackUserAdminMixin):
    list_display = (
        ...
        'hijack_field',  # Hijack button
    )
```

In addition, you should explicitly set `HIJACK_DISPLAY_ADMIN_BUTTON = False` in your project settings.

# Settings overview
## `HIJACK_DISPLAY_ADMIN_BUTTON`
Hide or display the "Hijack" buttons in the admin backend. Default: `True`.
## `HIJACK_BUTTON_TEMPLATE`
Path to template for the "Hijack" buttons in the admin backend. Default: `'hijack/admin_button.html'`
## `HIJACK_DISPLAY_WARNING`
Hide or display the yellow notificiation bar show to hijackers. Default: `True`.
## `HIJACK_USE_BOOTSTRAP`
Whether a Bootstrap-optimized notification bar is used. Default: `False`.
## `HIJACK_URL_ALLOWED_ATTRIBUTES`
User attributes by which a user can be hijacked over a URL. Default: `('user_id', 'email', 'username')`.
May be changed to a subset of the default value.
## `HIJACK_AUTHORIZE_STAFF`
Whether staff members are allowed to hijack. Default: `False`.
## `HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF`
Whether staff members are allowed to hijack other staff members. Default: `False`.
May not be True if `HIJACK_AUTHORIZE_STAFF` is disabled.
## `HIJACK_LOGIN_REDIRECT_URL`
URL a hijacker is redirected to when starting a hijack. Default: `settings.LOGIN_REDIRECT_URL`.
## `HIJACK_LOGOUT_REDIRECT_URL`
URL a hijacker is redirected to when ending a hijack. Default: `settings.LOGIN_REDIRECT_URL`.
## `HIJACK_AUTHORIZATION_CHECK`
Dotted path of a function checking whether `hijacker` is allowed to hijack `hijacked`. Default: `'hijack.helpers.is_authorized_default'`.
## `HIJACK_DECORATOR`
Dotted path of the decorator applied to the hijack views. Default: `'django.contrib.admin.views.decorators.staff_member_required'`.
