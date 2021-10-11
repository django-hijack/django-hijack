# Security Policy

## Preamble

Security is a vital part of any software that deal with authentication. Security will be
our first and last thought when considering contributions. We tried to keep this package
as small as possible to allow users as well as developers to comprehend security
implications.

## Reporting a Vulnerability

Please do not use GitHub's issue tracker for vulnerability reports. Please contact
maintainers directly via email available on their GitHub profiles.

## Security concepts for known risks

### Cross-Site-Request-Forging (CSRF)

We use the [csrf_protect][csrf_protect] decorator to enforce Django's CSRF protection
on all or views. This is also why we only support `POST` requests.

[csrf_protect]: https://docs.djangoproject.com/en/stable/ref/csrf/#django.views.decorators.csrf.csrf_protect

### Session injection / poisoning

Django's session engines, especially the `signed_cookies` engine, try to prevent session
injection as much as possible. However, you should make sure, that you do not use
user input as a session key anywhere in your application. An attacker could use this
as an attack vector.

### Misconfiguration

Configuration options are kept to a minimum. We prefer user extending behavior by the
means of inheritance to ensure a better understanding of the behavior.

Custom permission check method (`PERMISSION_CHECK`) require keyword arguments only
to avoid argument mismatching.

### Permission escalation

**Writing custom permission check functions is highly dangerous.**
If you create your own permission check, make sure to test your implementation against
all possible scenarios to prevent permission escalation.

### Undeliberate action

The built-in hijack notification can only be permanently hidden by setting the 
`HIJACK_INSERT_BEFORE` setting to `None`.
To protect users from performing operations as another user without their
knowledge, it should only be set to `None` if an equivalent global notification has been
built into your project - for example, in a project-wide layout file.

### Session expiration extension

Hijack does not extend a users original session life. If the original user is due
for reauthentication, the session will expire as it used to.


### Session leaking

Hijack uses Django's `login` utility function, that flushes the session every time
a users is being hijacked or released ensure that no session data leaks from one user
to another. The only exception is the session expiry which is transferred from one
session to another.
