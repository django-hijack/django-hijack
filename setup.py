import codecs
import os

from setuptools import setup, find_packages
import hijack as app


DESCRIPTION = (
    "allows superusers to hijack (login as) and work on behalf of another user"
)


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="django-hijack",
    version=app.__version__,
    description=DESCRIPTION,
    long_description=read("README.md"),
    long_description_content_type='text/markdown',
    license="The MIT License",
    platforms=["any"],
    keywords="django, hijack, support, customer support, debugging",
    author="arteria GmbH",
    author_email="admin@arteria.ch",
    url="https://github.com/arteria/django-hijack",
    project_urls={
        "Documentation": "https://django-hijack.readthedocs.io/",
        "Funding": "https://github.com/arteria/django-hijack#funding",
        "Source": "https://github.com/arteria/django-hijack",
        "Tracker": "https://github.com/arteria/django-hijack/issues",
    },
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 2.2",
        "Framework :: Django :: 3.0",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Software Development :: Libraries :: Application Frameworks",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
