# How to create your Sphinx documentation

In order to kickstart your Sphinx documentation, please do the following:

## Create virtual environment.

If you haven't done so already, create a virtual environment for this reusable
app like so:

    mkvirtualenv -p python2.7 django-hijack
    pip install Sphinx
    deactivate
    workon django-hijack
    sphinx-quickstart

Answer the questions:

    > Root path for the documentation [.]:
    > Separate source and build directories (y/N) [n]: y
    > Name prefix for templates and static dir [_]:
    > Project name: Django Hijack
    > Author name(s): arteria GmbH
    > Project version: 0.1
    > Project release [0.1]:
    > Source file suffix [.rst]:
    > Name of your master document (without suffix) [index]:
    > Do you want to use the epub builder (y/N) [n]:
    > autodoc: automatically insert docstrings from modules (y/N) [n]: y
    > doctest: automatically test code snippets in doctest blocks (y/N) [n]:
    > intersphinx: link between Sphinx documentation of different projects (y/N) [n]: y
    > todo: write "todo" entries that can be shown or hidden on build (y/N) [n]: y
    > coverage: checks for documentation coverage (y/N) [n]: y
    > pngmath: include math, rendered as PNG images (y/N) [n]:
    > mathjax: include math, rendered in the browser by MathJax (y/N) [n]:
    > ifconfig: conditional inclusion of content based on config values (y/N) [n]: y
    > viewcode: include links to the source code of documented Python objects (y/N) [n]: y
    > Create Makefile? (Y/n) [y]:
    > Create Windows command file? (Y/n) [y]:
