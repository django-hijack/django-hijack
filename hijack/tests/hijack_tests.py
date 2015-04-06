from django.test import TestCase
from django.core.urlresolvers import reverse
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from six.moves.urllib.parse import unquote

from django import VERSION

from django.test.client import Client


class HijackTests(TestCase):
    def setUp(self):
        admin_user, _ = User.objects.get_or_create(pk=1,
                                                   username='Admin',
                                                   email='admin@test.ch',
                                                   is_superuser=True,
                                                   is_staff=True, )
        if _:
            admin_user.set_password('Admin pw')
            admin_user.save()
        admin_user2, _ = User.objects.get_or_create(pk=4,
                                                    username='Admin2',
                                                    email='admin2@test.ch',
                                                    is_superuser=True,
                                                    is_staff=True, )
        if _:
            admin_user2.set_password('Admin2 pw')
            admin_user2.save()
        test1, _ = User.objects.get_or_create(pk=2,
                                              username='Test1',
                                              email='user1@test.ch',
                                              is_staff=True)
        if _:
            test1.set_password('Test1 pw')
            test1.save()
        test2, _ = User.objects.get_or_create(pk=3,
                                              username='Test2',
                                              email='user2@test.ch',
                                              is_staff=False)
        if _:
            test2.set_password('Test2 pw')
            test2.save()
        test3, _ = User.objects.get_or_create(pk=5,
                                              username='Test3',
                                              email='user3@test.ch',
                                              is_staff=True, )
        if _:
            test3.set_password('Test1 pw')
            test3.save()

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
        self.assertEqual(response.context['user'].username, 'Admin')

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
        self.assertRaises(self.client.get('/hijack/string/', follow=True))

    def test_hijack_helper_permission_denied(self):
        # relese hijack before hijack
        self.client.login(username='Admin', password='Admin pw')
        response = self.client.get('/hijack/release-hijack/', follow=True)
        self.assertEqual(response.status_code, 403)

        # hijack another admin user
        response = self.client.get('/hijack/5/', follow=True)
        self.assertEqual(response.status_code, 200)

        # check permision for hijack
        self.client.login(username='Test1', password='Test1 pw')

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
        delattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER')
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        # staff users should not be able to hijack admins
        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        # normal users should be ok
        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/3/', follow=True)
        self.assertEqual(response.status_code, 200)

        # other staff users should be ok
        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/5/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        self.client.login(username='Test2', password='Test2 pw')

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/1/', )
        print(response.status_code)
        if VERSION >= (1, 7):
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue(
                'name="this_is_the_login_form"' in str(response.content))

    def test_staff_to_staff_hijacking_without_proper_setting(self):
        self.client.login(username='Test1', password='Test1 pw')
        with self.settings(ALLOW_STAFF_TO_HIJACKUSER=True):
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 403)

    def test_staff_to_staff_hijacking_with_proper_setting(self):
        self.client.login(username='Test1', password='Test1 pw')
        with self.settings(ALLOW_STAFF_TO_HIJACKUSER=True,
                           ALLOW_STAFF_TO_HIJACK_STAFF_USER=True):
            response = self.client.get('/hijack/5/', follow=True)
            self.assertEqual(response.status_code, 200)

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
