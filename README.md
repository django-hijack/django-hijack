# Django Hijack

django-hijack allows superusers to hijack (=login as) and work on behalf of another user.

## Installation

To get the latest stable release from PyPi

    pip install django-hijack

To get the latest commit from GitHub

    pip install -e git+git://github.com/arteria/django-hijack.git#egg=hijack-master


In your ``settings.py`` add ``hijack`` to your ``INSTALLED_APPS`` and define ``LOGIN_REDIRECT_URL``

    INSTALLED_APPS = (
        ...,
        'hijack',
    )

    LOGIN_REDIRECT_URL = "/hello/"


Add the ``hijack`` URLs to your ``urls.py``

    urlpatterns = patterns('',
        ...
        url(r'^hijack/', include('hijack.urls')),
    )



## Usage and modes

There are different possibilies to hijack an user and communicate with users.

###  Hijack using the 'Hijack Button' in admin backend
Go to Users in the admin backend and push the ‘Hijack’ button to hijack an user. This is the default mode and base version 
of django-hijack.

### Hijack by calling URLs in the browser's address bar
For advanced superusers, users can be hijacked directly from the address bar by typing:

* example.com/hijack/``user-id``
* example.com/hijack/email/``email-address``
* example.com/hijack/username/``username``


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


# Signals

## Superuser logs in
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
* "got it" Link in notification to remove notification and flag from session. This is useful if hijack is used to switch between users and HIJACK_NOTIFY_ADMIN is True.

#Contribute

If you want to contribute to this project, simply send us a pull request. Thanks. :)
 

