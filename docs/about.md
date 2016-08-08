# TODOs, issues, and planned features
* Handle hijack using URLs on non-unique email addresses.
* Store info in user's profile (see #3 comments, Use case: 'Notify users when they were hijacked')
* Graceful support for custom user models that do not feature username / email

# Django 1.8–1.10 compatibility with [django-compat](https://github.com/arteria/django-compat)
All critical imports are carried out with the [compat library](https://github.com/arteria/django-compat) that ensures compatibility with Django 1.8 to 1.10.

The app is also tested with Django 1.4, 1.6, and 1.7. However, the tests are allowed to fail, and the package may not be fully compatible with those versions.

# Similar projects
Similar projects can be found and compared in the [user-switching](https://www.djangopackages.com/grids/g/user-switching/) or the [support](https://www.djangopackages.com/grids/g/support-apps/) grids at Django Packages.


# Contributing
If you want to contribute to this project, simply send us a pull request. Thanks. :)