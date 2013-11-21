# Django Hijack

django-hijack allows superusers to hijack (=login as) and work on behalf of another user.

## Installation

To get the latest stable release from PyPi

    pip install django-hijack

To get the latest commit from GitHub

    pip install -e git+git://github.com/arteria/django-hijack.git#egg=hijack


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

### Hijack by callign URLs in the browser's address bar
For advanced superusers, users can be hijacked directly from the address bar by typing:

* example.com/hijack/<user-id>
* example.com/hijack/email/<email-address>
* example.com/hijack/username/<username>
	
	
### Notify users when they were hijacked
This optional settings allows to notify and inform users when they were hijacked by a superuser. To activate this option 
follow these steps:

* In your base.html add ``{{ load hijack_tags }}``
* In your project settings add ``HIJACK_NOTIFY_USER = True``  (default is False) 

### Notify superusers when working behalf of another user
This optional settings warns the superuser that he/she is working with another user as initally logged in. To activate 
this option perform the following steps:

* In your base.html add ``{{ load hijack_tags }}`` (in not already done)
* In your project settings add ``HIJACK_NOTIFY_ADMIN = True`` (default is True) 
 

# Signals

## Superuser logs in
You can catch a signal when a superuser logs in as another user. Here is an example:
 
	from signals import post_superuser_login
	
    @receiver(post_superuser_login)
    def set_superuser(sender, **kwargs):
		print "Superuser hijacked userID %s" % kwargs['user_id']
        
		
		
		
# TODOs, know issues and planned features
* Handle hijack using URLs on non unique email addresses.


#Contribute

If you want to contribute to this project, simply send us a pull request. Thanks. :)
 

