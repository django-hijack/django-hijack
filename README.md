# Django Hijack

[![Build Status](https://travis-ci.org/arteria/django-hijack.svg?branch=master)](https://travis-ci.org/arteria/django-hijack)


![Screenshot of Hijack in action on the admin site.](https://www.arteria.ch/media/imgbucket/hijack_1.png)

[django-hijack](https://github.com/arteria/django-hijack) allows superusers to hijack (=login as) and work on behalf of other users without knowing their credentials.

## Table of contents

- [Installation](#installation)
- [Usage and modes](#usage-and-modes)
    - [Hijack Button](#hijack-using-the-hijack-button-on-the-admin-site)
    - [Hijack over url](#hijack-by-calling-urls-in-the-browsers-address-bar)
    - [Notify when logged in as a hijacked user](#notify-superusers-when-working-behalf-of-another-user)
    - [Release the hijack](#releasereverse-hijack)
        - [Hijack-History](#hijack-history)
    - [Notify user when they were hijacked](#notify-users-when-they-were-hijacked)
    - [Allow staff to hijack](#allow-staff-members-to-hijack-other-users)
    - [Django 1.4 to 1.8 compatibility with django-compat](#django-14---18-compatibility-with-django-compat)
    - [Custom user models](#support-for-custom-user-models)
- [Settings](#settings)
- [Signals](#signals)
    - [Hijacked](#superuser-logs-in)
- [TODOs, issues, planned features](#todos-issues-and-planned-features)
- [FAQ, troubleshooting and hints](#faq-troubleshooting-and-hints)
    - [SHOW_HIJACKUSER_IN_ADMIN not working](#why-does-the-hijack-button-not-show-up-in-the-admin-site-even-if-i-set-show_hijackuser_in_admin--true-in-my-project-settings)
- [Similar projects](#similar-projects)
- [Contribute](#contribute)

## Installation

To get the latest stable release from PyPi

    pip install django-hijack

To get the latest commit from GitHub

    pip install -e git+git://github.com/arteria/django-hijack.git#egg=hijack-master


In your ``settings.py`` add ``hijack`` to your ``INSTALLED_APPS`` and define ``LOGIN_REDIRECT_URL``

    INSTALLED_APPS = (
        ...,
        'hijack',
        'compat',
    )

You can specify a `HIJACK_LOGIN_REDIRECT_URL` and a `REVERSE_HIJACK_LOGIN_REDIRECT_URL`. This settings are used to redirect to a specific url after hijacking or releasing the user. Default for both is the django `LOGIN_REDIRECT_URL`.

    HIJACK_LOGIN_REDIRECT_URL = "/profile/"  # where you want to be redirected to, after hijacking the user.
    REVERSE_HIJACK_LOGIN_REDIRECT_URL = "/admin/"  # where you want to be redirected to, after releasing the user.


Add the ``hijack`` URLs to your ``urls.py``

    urlpatterns = patterns('',
        ...
        url(r'^hijack/', include('hijack.urls')),
    )

## Usage and modes

There are different possibilities to hijack a user and communicate with users.

###  Hijack using the 'Hijack Button' on the admin site
Go to Users in the admin backend and push the ‘Hijack’ button to hijack a user. This is the default mode and base version
of django-hijack. To disable the ‘Hijack’ button on the admin site (by not registrating the HijackUserAdmin) set ``SHOW_HIJACKUSER_IN_ADMIN = False`` in your project settings. If you are using a custom user model, you will have to add support for displaying the button yourself to your own `CustomUserAdmin`. Simply mix in the `hijack.admin.HijackUserAdminMixin`, and add `hijack_field` to `list_display`.


### Hijack by calling URLs in the browser's address bar
For advanced superusers, users can be hijacked directly from the address bar by typing:

* example.com/hijack/``user-id``
* example.com/hijack/email/``email-address``
* example.com/hijack/username/``username``

### Specify which user attributes are allowed to hijack on
By default all of the above methods (user id, email and username) are allowed. If you want to allow only a subset of these
you can set ALLOWED_HIJACKING_USER_ATTRIBUTES in your project settings. This will disable the other endpoints.
The settings take a list of methods to allow, you can select
from:

* user_ui
* email
* username

NOTE: The link on the admin page will change in the order listed above. Say that you have enabled *username* and *email* then
the users email will be used for the hijack link in on the admin page.

### Notify superusers when working behalf of another user
This option warns the superuser when working with another user as initally logged in. To activate this option perform
the following steps:

* In your base.html add ``{% load hijack_tags %}``, ``{%  load staticfiles %}`` and
* load the styles using ``<link rel="stylesheet" type="text/css" href="{% static 'hijack/hijack-styles.css' %}" />``.
* Place ``{{ request|hijackNotification }}`` just after your opening body tag.
* In your project settings add ``HIJACK_NOTIFY_ADMIN = True``. The default is True.
* You need to add ``django.core.context_processors.request`` to your template context processors to be able to use requests and sessions in the templates.
* Make sure that ``django.contrib.staticfiles`` is included in your ``INSTALLED_APPS``.
* Do not forget to run ``python manage.py collectstatic``.

### Release/reverse hijack

In the visual notification for the superuser (or staff if ``ALLOW_STAFF_TO_HIJACKUSER`` is True), when working on behalf of other users, there
is a link to release the hijacked user and switch back. After releasing you are redirected to `LOGIN_REDIRECT_URL` or to the URL defined in `REVERSE_HIJACK_LOGIN_REDIRECT_URL`.

    REVERSE_HIJACK_LOGIN_REDIRECT_URL = '/admin/auth/user/'

The release/reverse hijack will be executed when the URL `/hijack/release-hijack/` is called (or whatever is linked to the URL with name = "release_hijack").

#### Hijack history
If you (A) hijack a superuser (B) and then you hijack another user (C), the release will go backwards through the
 list of hijacked users one by one. After the first release you then are superuser (B), after the second you are superuser (A).



### Notify users when they were hijacked
NOTE: This use case is not fully implemented yet!

This option allows to notify and inform users when they were hijacked by a superuser. To activate this option
follow these steps:

* In your base.html add ``{% load hijack_tags %}``, ``{%  load staticfiles %}`` and
* load the styles using ``<link rel="stylesheet" type="text/css" href="{% static 'hijack/hijack-styles.css' %}" />``.
* Place ``{{ request|hijackNotification }}`` just after your opening body tag.
* In your project settings add ``HIJACK_NOTIFY_USER = True``. The default is False (= silent mode)
* You need to add ``django.core.context_processors.request`` to your template context processors to be able to use requests and sessions in the templates.
* Make sure that ``django.contrib.staticfiles`` is included in your ``INSTALLED_APPS``.
* Do not forget to run ``python manage.py collectstatic``.


### Allow staff members to hijack other users
This option allows staff members to hijack other users. In your project settings set ``ALLOW_STAFF_TO_HIJACKUSER`` to ``True``. The default is False.

### Django 1.4 - 1.8 compatibility with [django-compat](https://github.com/arteria/django-compat)

All critical imports are carried out with the [compat library](https://github.com/arteria/django-compat) that gives the compatibility for django 1.4 to 1.8

### Support for custom user models

django-hijack supports custom user models, all you need to do is to add the hijack button to your custom user `admin.py`. Import HijackUserAdminMixin from hijack admin and add ``hijack_field`` to your ``list_display``.

    # .. imports ..
    from hijack.admin import HijackUserAdminMixin

    class CustomUserAdmin(UserAdmin, HijackUserAdminMixin):
        # .. code ..
        list_display = ('email', 'first_name', 'last_name', 'is_staff', 'hijack_field')

## Settings

All configuration settings with their default value and description

    # Hijack button in admin user view; default = True
    SHOW_HIJACKUSER_IN_ADMIN = True
    
    # Notification for the admin if he is working for an other user; default = True
    HIJACK_NOTIFY_ADMIN = True
    
    # Allow staff users to hijack; default = False
    ALLOW_STAFF_TO_HIJACKUSER = False
    
    # Where to go when you hijack someone; default equals the LOGIN_REDIRECT_URL; which has the default '/accounts/profile/'
    REVERSE_HIJACK_LOGIN_REDIRECT_URL = LOGIN_REDIRECT_URL
    
    # Which methods of hijacking a user is allowed; default = ('user_id', 'email', 'username')
    ALLOWED_HIJACKING_USER_ATTRIBUTES = ('user_id', 'email', 'username')


## Signals

### Superuser logs in
You can catch a signal when a superuser logs in as another user. Here is an example:

    from django.dispatch import receiver
    from signals import post_superuser_login

    @receiver(post_superuser_login)
    def set_superuser(sender, **kwargs):
        print "Superuser hijacked userID %s" % kwargs['user_id']


# TODOs, issues and planned features
* Handle hijack using URLs on non unique email addresses.
* unset_superuser example for signals
* Store info in user's profile (see #3 comments, Use case: 'Notify users when they were hijacked', see above)
* "got it" Link in notification to remove notification and flag from session. This is useful if hijack is used to switch between users and ``HIJACK_NOTIFY_ADMIN`` is True.
* Support for named URLs for the hijack button.
* Handle signals in ``release_hijack(..)``, currently the signals are only triggered in ``login_user(..)`` and ``logout_user(..)``.
* Graceful support for custom user models that do not feature username / email

## FAQ, troubleshooting and hints

### Why does the hijack button not show up in the admin site, even if I set ``SHOW_HIJACKUSER_IN_ADMIN = True`` in my project settings?

If your ``UserAdmin`` object is already registered in the admin site through another app (here is an example of a Facebook profile, https://github.com/philippeowagner/django_facebook_oauth/blob/master/facebook/admin.py#L8), you could disable the registration of django-hijack by settings ``SHOW_HIJACKUSER_IN_ADMIN = False`` in your project settings.

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


## Similar projects

Similar projects can be found and compared in the [user-switching](https://www.djangopackages.com/grids/g/user-switching/) or the [support gird](https://www.djangopackages.com/grids/g/support-apps/) of djangopackages.


## Contribute

If you want to contribute to this project, simply send us a pull request. Thanks. :)
