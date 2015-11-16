# Installation

Get the latest stable release from PyPi:

    pip install django-hijack

In your ``settings.py``, add ``hijack`` and the dependency `compat` to your installed apps:

```python
INSTALLED_APPS = (
    ...,
    'hijack',
    'compat',
)
```

Finally, add the Django Hijack URLs to ``urls.py``:

```python
urlpatterns = patterns('',
    ...
    url(r'^hijack/', include('hijack.urls')),
)
```

## After installing

### Setting redirect URLs
You should specify a `HIJACK_LOGIN_REDIRECT_URL` and a `HIJACK_LOGOUT_REDIRECT_URL`. 
Admins are redirected there after hijacking or releasing a user. 
Both settings default to `LOGIN_REDIRECT_URL`.

```python
# settings.py
HIJACK_LOGIN_REDIRECT_URL = '/profile/'  # Where admins are redirected to after hijacking a user
HIJACK_LOGOUT_REDIRECT_URL = '/admin/auth/user/'  # Where admins are redirected to after releasing a user
```

### Notification bar
It is strongly recommended to display a notification bar to admins hijacking another user. This reduces the risk of an admin hijacking someone inadvertently or forgetting to release the user afterwards.
Setting up the notification bar requires the following steps:

* Add `django.core.context_processors.request` to your template context processors
* Add the following lines to your base.html:

```html
<!-- At the top -->
{% load staticfiles %}
{% load hijack_tags %}

...

<!-- In the head -->
<link rel="stylesheet" type="text/css" href="{% static 'hijack/hijack-styles.css' %}" />

...

<!-- Directly after <body> -->
{{ request | hijackNotification }}

...
```
* Make sure that ``django.contrib.staticfiles`` is included in your ``INSTALLED_APPS``, and do not forget to run ``python manage.py collectstatic``.

### Remote users
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

# Django 1.7 - 1.9 compatibility with [django-compat](https://github.com/arteria/django-compat)
All critical imports are carried out with the [compat library](https://github.com/arteria/django-compat) that ensures compatibility with Django 1.7 to 1.9.
The app is also tested with Django 1.4 and 1.6. However, those tests are allowed to fail, and the package may not be fully compatible with those versions.

# Usage

Superusers can hijack a user by clicking the "Hijack" button in the Users admin or more directly by sending a GET request to a `/hijack/...` URL.
If the hijacking is successful, you are redirected to the `HIJACK_LOGIN_REDIRECT_URL` 
and a yellow notification bar is displayed at the top of the landing page.

## Hijack button

By default, Django Hijack displays a button in the Django admin's user list, which usually is located at `/admin/auth/user/`. 
For instance, if you would like to hijack a user with the username "Max", click on the button named "Hijack Max".
You can hide the buttons by setting `HIJACK_DISPLAY_ADMIN_BUTTON = False` in your project settings.

## Hijack by calling URLs in the browser's address bar
Alternatively, you can hijack a user directly from the address bar by specifying their ID, username, or e-mail address.

* `example.com/hijack/<user-id>` 
* `example.com/hijack/username/<username>`
* `example.com/hijack/email/<email-address>`

## Ending the hijack
In order to end the hijack and switch back to your admin account, push the "Release" button in the yellow notification bar:

![Screenshot of the release button in the notification bar](release-button.png)

As an alternative, navigate directly to `/hijack/release-hijack/`.
After releasing, you are redirected to the `HIJACK_LOGOUT_REDIRECT_URL`.


# Advanced configuration

## Notification bar
Make sure that you have followed the steps in the "Installation" section. Django Hijack will then
display a yellow notification bar that warns admins when they are in the process of hijacking someone.
The template used for the notification bar is named "hijack/notifications.html", or "hijack/notifications_bootstrap.html" 
if Bootstrap is enabled.

### Bootstrap
If your project uses Bootstrap, you may want to set `HIJACK_USE_BOOTSTRAP = True` in your project settings.
Django Hijack will use a Bootstrap notification bar that does not overlap with the default navbar.

### Disabling the notification bar
You may temporarily disable the notification bar by setting `HIJACK_DISPLAY_WARNING = False`. 

## Permissions
By default, only superusers are allowed to hijack other users.
Django Hijack gives you a variety of options to extend the group of authorized users.

### Staff members
Set `HIJACK_AUTHORIZE_STAFF = True` in your project settings to authorize staff members to hijack non-staff users.
If you want staff to be able to hijack other staff as well, enable `HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF`.
Note that there is no option to authorize staff members to hijack superusers as this would undermine the distinction between staff users and superusers.

### Custom authorization function
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

:warning: The setting `HIJACK_AUTHORIZATION_CHECK` overrides the other hijack authorization settings. Defining a custom authorization function can have dangerous
effects on your application's authorization system. Potentially, it might allow any user to impersonate 
any other user and to take advantage of all their permissions.

### Custom view decorator
Django Hijack's views are decorated by Django's `staff_member_required` decorator. If you have written your own 
authorization function, or haven't installed `django.contrib.admin`, you may want to override this behaviour by 
setting `HIJACK_DECORATOR` to the dotted path of a custom decorator. Example:

```python
HIJACK_DECORATOR = 'mysite.decorators.mydecorator'
```

## Custom user models
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


# Signals

## Superuser logs in
You can catch a signal when a superuser logs in as another user. Here is an example:

    from django.dispatch import receiver
    from signals import post_superuser_login

    @receiver(post_superuser_login)
    def set_superuser(sender, **kwargs):
        print "Superuser hijacked userID %s" % kwargs['user_id']


# TODOs, issues, and planned features
* Handle hijack using URLs on non-unique email addresses.
* unset_superuser example for signals
* Store info in user's profile (see #3 comments, Use case: 'Notify users when they were hijacked')
* "got it" Link in notification to remove notification and flag from session. This is useful if hijack is used to switch between users and ``HIJACK_DISPLAY_WARNING`` is True.
* Support for named URLs for the hijack button.
* Handle signals in ``release_hijack(..)``, currently the signals are only triggered in ``login_user(..)`` and ``logout_user(..)``.
* Graceful support for custom user models that do not feature username / email


# FAQ, troubleshooting and hints

## Why does the hijack button not show up in the admin site, even if I set ``HIJACK_DISPLAY_ADMIN_BUTTON = True`` in my project settings?

If your ``UserAdmin`` object is already registered in the admin site through another app (here is an example of a Facebook profile, https://github.com/philippeowagner/django_facebook_oauth/blob/master/facebook/admin.py#L8), you can disable the registration of django-hijack by settings ``HIJACK_DISPLAY_ADMIN_BUTTON = False`` in your project settings.

Afterwards create a new ``UserAdmin`` class derived from ``HijackUserAdmin``. The Facebook example would look like this:


    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin
    from django.contrib.auth.models import User

    from hijack.admin import HijackUserAdmin

    from .models import FacebookProfile

    # We want to display our facebook profile, not the default user's profile
    admin.site.unregister(User)

    class FacebookProfileInline(admin.StackedInline):
        model = FacebookProfile

    class FacebookProfileAdmin(HijackUserAdmin):
        inlines = [FacebookProfileInline]

    admin.site.register(User, FacebookProfileAdmin)


# Similar projects

Similar projects can be found and compared in the [user-switching](https://www.djangopackages.com/grids/g/user-switching/) or the [support gird](https://www.djangopackages.com/grids/g/support-apps/) categories of Django Packages.


# Contribute

If you want to contribute to this project, simply send us a pull request. Thanks. :)