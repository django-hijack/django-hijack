from six.moves.urllib.parse import unquote

from django import VERSION
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from django.test import TestCase
from django.test.utils import override_settings
from django.test.client import Client

from hijack import settings as hijack_settings
from hijack.tests.utils import SettingsOverride
from hijack.templatetags.hijack_tags import can_hijack

class HijackTests(TestCase):
    def setUp(self):
        self.admin_user, _ = User.objects.get_or_create(pk=1,
                                                   username='Admin',
                                                   email='admin@test.ch',
                                                   is_superuser=True,
                                                   is_staff=True, )
        if _:
            self.admin_user.set_password('Admin pw')
            self.admin_user.save()
        self.admin_user2, _ = User.objects.get_or_create(pk=4,
                                                    username='Admin2',
                                                    email='admin2@test.ch',
                                                    is_superuser=True,
                                                    is_staff=True, )
        if _:
            self.admin_user2.set_password('Admin2 pw')
            self.admin_user2.save()
        self.test1, _ = User.objects.get_or_create(pk=2,
                                              username='Test1',
                                              email='user1@test.ch',
                                              is_staff=True)
        if _:
            self.test1.set_password('Test1 pw')
            self.test1.save()
        self.test2, _ = User.objects.get_or_create(pk=3,
                                              username='Test2',
                                              email='user2@test.ch',
                                              is_staff=False)
        if _:
            self.test2.set_password('Test2 pw')
            self.test2.save()
        self.test3, _ = User.objects.get_or_create(pk=5,
                                              username='Test3',
                                              email='user3@test.ch',
                                              is_staff=True, )
        if _:
            self.test3.set_password('Test1 pw')
            self.test3.save()

        self.client = Client()

    def test_login(self):
        self.assertFalse(self.client.login(username='name', password='pw'))
        self.assertTrue(self.client.login(username='Admin',
                                          password='Admin pw'))
        self.assertTrue(self.client.login(username='Test2',
                                          password='Test2 pw'))

    def test_hijack_simple(self):
        self.client.login(username='Admin', password='Admin pw')
        response = self.client.get('/hijack/2/', follow=True)
        self.assertTrue(
            'on behalf of %s' %
            (response.context['user'].username) in str(response.content))

        response = self.client.get('/hijack/release-hijack/', follow=True)
        self.assertEqual(response.context['username'], 'Admin')

        response = self.client.get('/hijack/3/', follow=True)
        self.assertTrue(
            'on behalf of %s' %
            (response.context['user'].username) in str(response.content))

        response = self.client.get(
            '/hijack/disable-hijack-warning/?next=/hello',
            follow=True)
        self.assertFalse(
            'on behalf of %s' %
            (response.context['user'].username) in str(response.content))

        self.client.logout()

    def test_hijack_email(self):
        self.client.login(username='Admin', password='Admin pw')
        response = self.client.get('/hijack/email/user2@test.ch/', follow=True)
        self.assertEqual(response.context['user'].username, 'Test2')

    def test_hijack_username(self):
        self.client.login(username='Admin', password='Admin pw')
        response = self.client.get('/hijack/username/Test1/', follow=True)
        self.assertEqual(response.context['user'].username, 'Test1')

    def test_hijack_view_error(self):
        self.client.login(username='Admin', password='Admin pw')
        response = self.client.get('/hijack/string/', follow=True)
        self.assertEqual(response.status_code, 400)

    def test_hijack_helper_permission_denied(self):
        # release hijack before hijack
        self.client.login(username='Admin', password='Admin pw')
        response = self.client.get('/hijack/release-hijack/', follow=True)
        self.assertEqual(response.status_code, 403)

        # hijack another admin user
        response = self.client.get('/hijack/5/', follow=True)
        self.assertEqual(response.status_code, 200)

        # check permision for hijack
        self.client.login(username='Test1', password='Test1 pw')

        setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
        delattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER')
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        # staff users should not be able to hijack admins
        setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        # normal users should be ok
        setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/3/', follow=True)
        self.assertEqual(response.status_code, 200)

        # other staff users should be ok
        setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/5/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        self.client.login(username='Test2', password='Test2 pw')

        setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/1/', )

        if VERSION >= (1, 7):
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(
                'name="this_is_the_login_form"' in str(response.content))

    def test_hijacking_inactive_user(self):
        self.client.login(username='Admin', password='Admin pw')
        self.test1.is_active = False
        self.test1.save()
        response = self.client.get('/hijack/%d/' % self.test1.id, follow=True)
        self.assertEqual(response.status_code, 403)
        self.client.logout()

    def test_staff_to_staff_hijacking_without_proper_setting(self):
        self.client.login(username='Test1', password='Test1 pw')
        with SettingsOverride(hijack_settings, ALLOW_STAFF_TO_HIJACKUSER=True):
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 403)

    def test_staff_to_staff_hijacking_with_proper_setting(self):
        self.client.login(username='Test1', password='Test1 pw')
        with SettingsOverride(hijack_settings, ALLOW_STAFF_TO_HIJACKUSER=True,
                           ALLOW_STAFF_TO_HIJACK_STAFF_USER=True):
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 200)

    def test_staff_to_admin_hijacking_never_allowed(self):
        # a staff user should never hijack an admin
        self.client.login(username='Test1', password='Test1 pw')
        with SettingsOverride(hijack_settings, ALLOW_STAFF_TO_HIJACK_STAFF_USER=True):
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 403)

    def test_hijack_admin(self):
        from hijack.admin import HijackUserAdmin

        ua = HijackUserAdmin(User, AdminSite())
        self.assertEqual(ua.list_display,
                         ('username', 'email', 'first_name', 'last_name',
                          'last_login', 'date_joined', 'is_staff',
                          'hijack_field', ))

    def test_hijack_urls(self):
        self.assertEqual('/hijack/disable-hijack-warning/',
                         reverse('disable_hijack_warning'))
        self.assertEqual('/hijack/release-hijack/', reverse('release_hijack'))
        self.assertEqual('/hijack/1/', reverse('login_with_id', args=[1]))
        self.assertEqual('/hijack/2/', reverse('login_with_id',
                                               kwargs={'user_id': 2}))
        self.assertEqual('/hijack/username/bob/',
                         reverse('login_with_username',
                                 args=['bob']))
        self.assertEqual('/hijack/username/bob_too/',
                         reverse('login_with_username',
                                 kwargs={'username': 'bob_too'}))
        self.assertEqual('/hijack/email/bob@bobsburgers.com/',
                         unquote(reverse('login_with_email',
                                         args=['bob@bobsburgers.com'])))
        self.assertEqual('/hijack/email/bob_too@bobsburgers.com/', unquote(
            reverse('login_with_email',
                    kwargs={'email': 'bob_too@bobsburgers.com'})))

    def test_hijack_always_yes(self):
        with SettingsOverride(hijack_settings, CUSTOM_HIJACK_HANDLER='hijack.tests.test_app.custom_hijack.can_hijack_yes'):
            # release hijack before hijack
            self.client.login(username='Admin', password='Admin pw')
            response = self.client.get('/hijack/release-hijack/', follow=True)
            self.assertEqual(response.status_code, 403)

            # hijack another admin user
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 200)

            # check permision for hijack
            self.client.login(username='Test1', password='Test1 pw')

            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
            delattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER')
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 200)

            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 200)

            # staff users should not be able to hijack admins
            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 200)

            # normal users should be ok
            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
            response = self.client.get('/hijack/3/', follow=True)
            self.assertEqual(response.status_code, 200)

            # other staff users should be ok
            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 200)

    def test_hijack_always_no(self):
        with SettingsOverride(hijack_settings, CUSTOM_HIJACK_HANDLER='hijack.tests.test_app.custom_hijack.can_hijack_no'):
            # release hijack before hijack
            self.client.login(username='Admin', password='Admin pw')
            response = self.client.get('/hijack/release-hijack/', follow=True)
            self.assertEqual(response.status_code, 403)

            # hijack another admin user
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 403)

            # check permision for hijack
            self.client.login(username='Test1', password='Test1 pw')

            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
            delattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER')
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 403)

            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 403)

            # staff users should not be able to hijack admins
            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
            response = self.client.get('/hijack/1/', follow=True)
            self.assertEqual(response.status_code, 403)

            # normal users should be ok
            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
            response = self.client.get('/hijack/3/', follow=True)
            self.assertEqual(response.status_code, 403)

            # other staff users should be ok
            setattr(hijack_settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 403)

    def test_can_hijack_filter(self):
        admin1 = User.objects.get(pk=1)
        admin2 = User.objects.get(pk=5)
        self.assertEqual(can_hijack(admin1, admin2), True)

    def test_last_login_not_changed(self):
        self.client.login(username='Test1', password='Test1 pw')
        self.client.logout()
        last_login = User.objects.get(pk=self.test1.pk).last_login
        self.assertIsNotNone(last_login)
        self.client.login(username='Admin', password='Admin pw')
        self.client.get('/hijack/%d/' % self.test1.pk, follow=True)
        self.client.logout()
        self.assertEqual(last_login, User.objects.get(pk=self.test1.pk).last_login)


@override_settings(CUSTOM_HIJACK_HANDLER='hijack.tests.test_app.custom_hijack.can_hijack_default')
class DefaultCustomHijackTests(HijackTests):
    pass

if VERSION >= (1, 7):
    from django.core.checks import Error
    from hijack import checks
    from hijack.apps import HijackConfig


    class ChecksTests(TestCase):

        def test_check_allowed_hijacking_user_attributes(self):
            errors = checks.check_allowed_hijacking_user_attributes(HijackConfig)
            self.assertFalse(errors)

            with SettingsOverride(hijack_settings, ALLOWED_HIJACKING_USER_ATTRIBUTES=('username',)):
                errors = checks.check_allowed_hijacking_user_attributes(HijackConfig)
                self.assertFalse(errors)

            with SettingsOverride(hijack_settings, ALLOWED_HIJACKING_USER_ATTRIBUTES=('username', 'email')):
                errors = checks.check_allowed_hijacking_user_attributes(HijackConfig)
                self.assertFalse(errors)

            with SettingsOverride(hijack_settings, ALLOWED_HIJACKING_USER_ATTRIBUTES=('other',)):
                errors = checks.check_allowed_hijacking_user_attributes(HijackConfig)
                expected_errors = [
                    Error(
                        'Setting ALLOWED_HIJACKING_USER_ATTRIBUTES needs to be '
                        'subset of (user_id, email, username)',
                        hint=None,
                        obj=hijack_settings.ALLOWED_HIJACKING_USER_ATTRIBUTES,
                        id='hijack.E001',
                    )
                ]
                self.assertEqual(errors, expected_errors)

        def test_check_show_hijackuser_in_admin_with_custom_user_model(self):
            warnings = checks.check_show_hijackuser_in_admin_with_custom_user_model(HijackConfig)
            self.assertFalse(warnings)

            with SettingsOverride(hijack_settings, SHOW_HIJACKUSER_IN_ADMIN=False):
                warnings = checks.check_show_hijackuser_in_admin_with_custom_user_model(HijackConfig)
                self.assertFalse(warnings)

            with SettingsOverride(hijack_settings, SHOW_HIJACKUSER_IN_ADMIN=True):
                warnings = checks.check_show_hijackuser_in_admin_with_custom_user_model(HijackConfig)
                self.assertFalse(warnings)
