from django import forms
from django.contrib.staticfiles.storage import staticfiles_storage


class Asset:
    """Represent a static asset referenced by its path.

    Wraps a static file path so it can be compared, hashed and rendered
    lazily. The resolved URL is only looked up via the staticfiles storage
    when the asset is converted to a string.
    """

    def __init__(self, path):
        self.path = path

    def __eq__(self, other):
        # Allow comparison against both plain path strings and other Assets.
        if isinstance(other, Asset):
            return self.path == other.path
        return self.path == other

    def __hash__(self):
        # Hash by path so Assets behave like their underlying path string
        # (and can be deduplicated in sets/dicts alongside plain strings).
        return hash(self.path)

    def __str__(self):
        return staticfiles_storage.url(self.path)
