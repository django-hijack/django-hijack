Django Hijack
============

django-hijack allows superusers to hijack (=login as) and work on behalf of another user.

Installation
------------

To get the latest stable release from PyPi

.. code-block:: bash

    pip install django-hijack

To get the latest commit from GitHub

.. code-block:: bash

    pip install -e git+git://github.com/arteria/django-hijack.git#egg=hijack


In your ``settings.py`` add ``hijack`` to your ``INSTALLED_APPS`` and define ``LOGIN_REDIRECT_URL``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'hijack',
    )
    
    LOGIN_REDIRECT_URL = "/hello/"
    

Add the ``hijack`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^hijack/', include('hijack.urls')),
    )




Usage
-----

Go to Users in the admin interface and push the ‘Hijack’ button to hijack an user.


Contribute
----------

If you want to contribute to this project, please perform the following steps

.. code-block:: bash

    # Fork this repository
    # Clone your fork
    mkvirtualenv -p python2.7 django-hijack
    make develop

    git co -b feature_branch master
    # Implement your feature and tests
    git add . && git commit
    git push -u origin feature_branch
    # Send us a pull request for your feature branch


.. image:: https://d2weczhvl823v0.cloudfront.net/philippeowagner/django-hijack/trend.png
   :alt: Bitdeli badge
   :target: https://bitdeli.com/free

