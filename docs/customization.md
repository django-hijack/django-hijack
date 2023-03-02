# Customization

## Hijack permission

By default, only superusers are allowed to hijack other users. This behavior
can be adapted to your liking. However, be aware of the potential security implications.

You alter the permission check, including that of the `can_hijack` template tag via the
`HIJACK_PERMISSION_CHECK` setting.

The setting is a dotted/Python path to permission function.
The function must accept two keyword arguments `hijacker` and `hijacked`.
Default: `'hijack.permissions.superusers_only'`.

### Builtin permission functions

We provide a couple of builtin permission functions for your convenience.

#### `hijack.permissions.superusers_only`

A superuser may hijack any other user (except inactive ones).
Used by default.

#### `hijack.permissions.superusers_and_staff`

Superusers and staff members may hijack other users (except inactive ones).

A superuser may hijack any other user.
A staff member may hijack any user, except another staff member or superuser.

Can be enabled by changing your settings to:

```python
# settings.py
HIJACK_PERMISSION_CHECK = "hijack.permissions.superusers_and_staff"
```

### Custom permission functions

Advanced Django developers might want to define their own check whether a user may
hijack another user. This can be achieved by writing a custom permission function.
The function must accept two keyword arguments `hijacker` and `hijacked` and return
a boolean value. Example:

```python
# mysite/permissions.py

def hijack_superusers_only(*, hijacker, hijacked):
    """Only superusers may hijack other users."""
    return hijacked.is_active and hijacker.is_superuser


def hijack_staff_other_staff(*, hijacker, hijacked):
    """Staff members may hijack other staff and regular users, but not superusers."""
    if not hijacked.is_active:
        return False

    if hijacker.is_superuser:
        return True

    if hijacker.is_staff and not hijacked.is_superuser:
        return True
```

**Warning: Writing custom permission check functions is highly dangerous.**
If you create your own permission check, make sure to test your implementation against
all possible scenarios to prevent permission escalation.

Hijacking inactive users (i.e. users with `is_active=False`) is not allowed to prevent
dead locks, since an inactive user cannot be released.

## Notification Layout

There is no "one size fits all" solution, when it comes to the notification layout.
Therefore, it is recommended to create your own template and adapt the notification
to your site specific layout.

Create a template called `hijack/notification.html` in your template folder.

Use may use the default template as a cheat-sheet. If you are experiencing trouble,
please refer to Django's guide on [overriding templates][overriding-templates].

```html
<!-- hijack/notification.html -->
<link rel="stylesheet" type="text/css" href="{% static 'hijack/hijack.min.css' %}" media="screen">
<div class="djhj" id="djhj">
  <div class="djhj-notification">
    <div class="djhj-message">
      {% blocktrans trimmed with user=request.user %}
        You are currently working on behalf of <em>{{ user }}</em>.
      {% endblocktrans %}
    </div>
    <form action="{% url 'hijack:release' %}" method="POST" class="djhj-actions">
      {% csrf_token %}
      <input type="hidden" name="next" value="{{ request.path }}">
      <button class="djhj-button" onclick="document.getElementById('djhj').style.display = 'none';" type="button">
        {% trans 'hide' %}
      </button>
      <button class="djhj-button" type="submit">
        {% trans 'release' %}
      </button>
    </form>
  </div>
</div>
```

The `next` field is optional as well, but with a different default. If not provided
a user will be forwarded to the [LOGOUT_REDIRECT_URL][LOGOUT_REDIRECT_URL].

[overriding-templates]: https://docs.djangoproject.com/en/3.1/howto/overriding-templates/
[LOGOUT_REDIRECT_URL]: https://docs.djangoproject.com/en/stable/ref/settings/#logout-redirect-url

### Identifying hijacked users

A hijacked user can be identified in you template or application via
`request.user.is_hijacked`. This attribute will be true for hijacked users.

## Hijack admin button

You can override the hijack button that renders in the admin.

Create a template called hijack/contrib/admin/button.html in your template folder.
You can use the default template as a cheat-sheet.

```
{% load i18n l10n hijack %}

{% if request.user|can_hijack:another_user %}
  <button type="button" class="button" data-hijack-user="{{ another_user.pk|unlocalize }}"
          data-hijack-next="{{ next }}" data-hijack-url="{% url 'hijack:acquire' %}">
    {% if is_user_admin %}
      {% trans 'hijack'|upper %}
    {% else %}
      {% blocktrans %}Hijack {{ username }}{% endblocktrans %}
    {% endif %}
  </button>
{% endif %}
```

## Settings

### `HIJACK_INSERT_BEFORE`

Alters at which point of the DOM the notification is injected.  The notification will not be injected if set to `None`.

**Warning: Hiding the notification increases the risk of [undeliberate action](security.md#undeliberate-action).
Ensure your project has its own notification mechanism before setting this to `None`.**

Default: `</body>`.

### `HIJACK_PERMISSION_CHECK`
Dotted path of a function checking whether `hijacker` is allowed to hijack `hijacked`.
The function must accept two keyword arguments `hijacker` and `hijacked`.

Default: `'hijack.permissions.has_hijack_perm'`.

## Signals
You can catch a signal when someone is hijacked or released. Here is an example:

```python
from hijack import signals


def print_hijack_started(sender, hijacker, hijacked, request, **kwargs):
    print('%d has hijacked %d' % (hijacker, hijacked))
signals.hijack_started.connect(print_hijack_started)

def print_hijack_ended(sender, hijacker, hijacked, request, **kwargs):
    print('%d has released %d' % (hijacker, hijacked))
signals.hijack_ended.connect(print_hijack_ended)
```
