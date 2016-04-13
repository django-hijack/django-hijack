# -*- encoding: utf-8 -*-
"""
Python setup file for the hijack app.

In order to register your app at pypi.python.org, create an account at
pypi.python.org and login, then register your new app like so:

    python setup.py register

If your name is still free, you can now make your first release but first you
should check if you are uploading the correct files:

    python setup.py sdist

Inspect the output thoroughly. There shouldn't be any temp files and if your
app includes staticfiles or templates, make sure that they appear in the list.
If something is wrong, you need to edit MANIFEST.in and run the command again.

If all looks good, you can make your first release:

    python setup.py sdist upload

For new releases, you need to bump the version number in
hijack/__init__.py and re-run the above command.

For more information on creating source distributions, see
http://docs.python.org/2/distutils/sourcedist.html

"""
import os
from setuptools import setup, find_packages
import hijack as app

dev_requires = ['flake8', ]


def read(fname):
    try:
        return open(os.path.join(os.path.dirname(__file__), fname), 'r').read()
    except IOError:
        return u''


setup(name="django-hijack",
      version=app.__version__,
      description=read('DESCRIPTION'),
      long_description=read('README.md'),
      license='The MIT License',
      platforms=['OS Independent'],
      keywords='django, hijack, support, customer support, debugging',
      author='arteria GmbH',
      author_email='admin@arteria.ch',
      url="https://github.com/arteria/django-hijack",
      packages=find_packages(),
      include_package_data=True,
      install_requires=open('requirements.txt').read().split('\n'),
      extras_require={'dev': dev_requires, },
      classifiers=['Development Status :: 5 - Production/Stable',
                   'Framework :: Django',
                   'License :: OSI Approved :: MIT License',
                   'Framework :: Django',
                   'Framework :: Django :: 1.7',
                   'Framework :: Django :: 1.8',
                   'Framework :: Django :: 1.9',
                   'Programming Language :: Python',
                   'Programming Language :: Python :: 2',
                   'Programming Language :: Python :: 3', ], )
