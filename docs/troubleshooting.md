
# Why does the hijack button not show up in the admin site, even if I set ``HIJACK_DISPLAY_ADMIN_BUTTON = True`` in my project settings?

If your ``UserAdmin`` object is already registered in the admin site through another app (here is an example of a Facebook profile, https://github.com/philippeowagner/django_facebook_oauth/blob/master/facebook/admin.py#L8), you can disable the registration of django-hijack by settings ``HIJACK_DISPLAY_ADMIN_BUTTON = False`` in your project settings.

Afterwards create a new ``UserAdmin`` class derived from ``HijackUserAdmin``. The Facebook example would look like this:


    from django.contrib import admin
    from django.contrib.auth.admin import UserAdmin
    from django.contrib.auth.models import User

    from hijack.admin import HijackUserAdmin

    from .models import FacebookProfile

    # We want to display our facebook profile, not the default user's profile
    admin.site.unregister(User)

    class FacebookProfileInline(admin.StackedInline):
        model = FacebookProfile

    class FacebookProfileAdmin(HijackUserAdmin):
        inlines = [FacebookProfileInline]

    admin.site.register(User, FacebookProfileAdmin)
