# Troubleshooting

## Remote users

To work with `REMOTE_USER`, place `'hijack.middleware.HijackUserMiddleware'`
between `'django.contrib.auth.middleware.AuthenticationMiddleware'` and
`'django.contrib.auth.middleware.RemoteUserMiddleware'`:

```python
# settings.py

MIDDLEWARE_CLASSES = [
    # …
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "hijack.middleware.HijackUserMiddleware",
    "django.contrib.auth.middleware.RemoteUserMiddleware",
    # …
]
```

## Notification banner missing

Hijack can't insert the notification into a compressed response.
Place compression middleware, like `django.middleware.gzip.GZipMiddleware`,
above `'hijack.middleware.HijackUserMiddleware'`, so it compresses the response
after the banner was added:

```python
# settings.py

MIDDLEWARE = [
    "django.middleware.gzip.GZipMiddleware",
    # …
    "hijack.middleware.HijackUserMiddleware",
    # …
]
```
