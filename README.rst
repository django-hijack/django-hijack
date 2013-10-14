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

TODO: Describe further installation steps (edit / remove the examples below):

Add ``hijack`` to your ``INSTALLED_APPS``

.. code-block:: python

    INSTALLED_APPS = (
        ...,
        'hijack',
    )

Add the ``hijack`` URLs to your ``urls.py``

.. code-block:: python

    urlpatterns = patterns('',
        ...
        url(r'^hijack/', include('hijack.urls')),
    )

Before your tags/filters are available in your templates, load them by using

.. code-block:: html

	{% load hijack_tags %}


Don't forget to migrate your database

.. code-block:: bash

    ./manage.py migrate hijack


Usage
-----

TODO: Describe usage or point to docs. Also describe available settings and
templatetags.


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
