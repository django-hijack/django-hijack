# TODOs, issues, and planned features
* Handle hijack using URLs on non-unique email addresses.
* unset_superuser example for signals
* Store info in user's profile (see #3 comments, Use case: 'Notify users when they were hijacked')
* "got it" Link in notification to remove notification and flag from session. This is useful if hijack is used to switch between users and ``HIJACK_DISPLAY_WARNING`` is True.
* Support for named URLs for the hijack button.
* Handle signals in ``release_hijack(..)``, currently the signals are only triggered in ``login_user(..)`` and ``logout_user(..)``.
* Graceful support for custom user models that do not feature username / email

# Django 1.7–1.9 compatibility with [django-compat](https://github.com/arteria/django-compat)
All critical imports are carried out with the [compat library](https://github.com/arteria/django-compat) that ensures compatibility with Django 1.7 to 1.9.

The app is also tested with Django 1.4 and 1.6. However, the tests are allowed to fail, and the package may not be fully compatible with those versions.

# Similar projects
Similar projects can be found and compared in the [user-switching](https://www.djangopackages.com/grids/g/user-switching/) or the [support](https://www.djangopackages.com/grids/g/support-apps/) grids at Django Packages.


# Contributing
If you want to contribute to this project, simply send us a pull request. Thanks. :)