# Troubleshooting

## Remote users
To work with `REMOTE_USER`,  place `'hijack.middleware.HijackUserMiddleware'`
between `'django.contrib.auth.middleware.AuthenticationMiddleware'` and
`'django.contrib.auth.middleware.RemoteUserMiddleware'`:

```python
# settings.py

MIDDLEWARE_CLASSES = [
    # …
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'hijack.middleware.HijackUserMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
    # …
]
```
