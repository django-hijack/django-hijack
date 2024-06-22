from hijack import forms


class TestAsset:
    def test_init(self):
        asset = forms.Asset("path")
        assert asset.path == "path"

    def test_eq(self):
        asset = forms.Asset("path")
        assert asset == "path"
        assert asset == forms.Asset("path")
        assert asset != forms.Asset("other")

    def test_hash(self):
        asset = forms.Asset("path")
        assert hash(asset) == hash("path")

    def test_str(self, settings):
        settings.STORAGES = {
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
            },
        }
        asset = forms.Asset("path")
        assert str(asset) == "/static/path"

    def test_absolute_path(self, settings):
        settings.STORAGES = {
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
            },
        }
        asset = forms.Asset("path")
        assert asset.absolute_path("path") == "/static/path"
        assert asset.absolute_path("/path") == "/path"
        assert asset.absolute_path("http://path") == "http://path"
        assert asset.absolute_path("https://path") == "https://path"

    def test_repr(self):
        asset = forms.Asset("path")
        assert repr(asset) == "Asset: 'path'"


class TestESM:
    def test_str(self, settings):
        settings.STORAGES = {
            "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
            "staticfiles": {
                "BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"
            },
        }
        js = forms.ESM("path")
        assert str(js) == '<script src="/static/path" type="module"></script>'
