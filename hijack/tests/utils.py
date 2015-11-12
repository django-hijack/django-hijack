
# Borrowed from https://github.com/stefanfoulis/django-filer/blob/develop/filer/tests/helpers.py
class SettingsOverride(object):
    """
    Overrides Django settings within a context and resets them to their inital
    values on exit.
    Example:
        with SettingsOverride(DEBUG=True):
            # do something
    """

    def __init__(self, settings_module, **overrides):
        self.settings_module = settings_module
        self.overrides = overrides

    def __enter__(self):
        self.old = {}
        for key, value in list(self.overrides.items()):
            self.old[key] = getattr(self.settings_module, key, None)
            setattr(self.settings_module, key, value)

    def __exit__(self, _type, value, traceback):
        for key, value in list(self.old.items()):
            if value is not None:
                setattr(self.settings_module, key, value)
            else:
                delattr(self.settings_module, key)