from django.test import TestCase
from django.conf import settings
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite

from django import VERSION


from django.test.client import Client

class HijackTests(TestCase):

    def setUp(self):
        admin_user, _ = User.objects.get_or_create(pk=1, username='Admin', email='admin@test.ch', is_superuser=True, is_staff=True,)
        if _:
            admin_user.set_password('Admin pw')
            admin_user.save()
        test1, _ = User.objects.get_or_create(pk=2, username='Test1', email='user1@test.ch', is_staff=True)
        if _:
            test1.set_password('Test1 pw')
            test1.save()
        test2, _ = User.objects.get_or_create(pk=3, username='Test2', email='user2@test.ch', is_staff=False)
        if _:
            test2.set_password('Test2 pw')
            test2.save()

        self.client = Client()

    def test_login(self):
        self.assertFalse(self.client.login(username='name',password='pw'))
        self.assertTrue(self.client.login(username='Admin',password='Admin pw'))
        self.assertTrue(self.client.login(username='Test2',password='Test2 pw'))

    def test_hijack_simple(self):
        self.client.login(username='Admin',password='Admin pw')
        response = self.client.get('/hijack/2/', follow=True)
        self.assertTrue('on behalf of %s' % (response.context['user'].username) in str(response.content))
        
        response = self.client.get('/hijack/release-hijack/', follow=True)
        self.assertEqual(response.context['user'].username, 'Admin')
        
        response = self.client.get('/hijack/3/', follow=True)
        self.assertTrue('on behalf of %s' % (response.context['user'].username) in str(response.content))
        
        response = self.client.get('/hijack/disable-hijack-warning/?next=/hello', follow=True)
        self.assertFalse('on behalf of %s' % (response.context['user'].username) in str(response.content))

        self.client.logout()

        #self.client.login(username='Admin',password='Admin pw')
        #response = self.client.get('/hijack/3/', follow=True)
        #self.assertTrue('on behalf of %s' % (response.context['user'].username) in response.content)

    def test_hijack_email(self):
        self.client.login(username='Admin',password='Admin pw')
        response = self.client.get('/hijack/email/user2@test.ch/', follow=True)
        self.assertEqual(response.context['user'].username, 'Test2')

    def test_hijack_username(self):
        self.client.login(username='Admin',password='Admin pw')
        response = self.client.get('/hijack/username/Test1/', follow=True)
        self.assertEqual(response.context['user'].username, 'Test1')

    def test_hijack_view_error(self):
        self.client.login(username='Admin',password='Admin pw')
        self.assertRaises(self.client.get('/hijack/string/', follow=True))

    def test_hijack_helper_permission_denied(self):
        # relese hijack before hijack
        self.client.login(username='Admin',password='Admin pw')
        response = self.client.get('/hijack/release-hijack/', follow=True)
        self.assertEqual(response.status_code, 403)

        # check permision for hijack
        self.client.login(username='Test1',password='Test1 pw')

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
        delattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER')
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', False)
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 403)

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/1/', follow=True)
        self.assertEqual(response.status_code, 200)

        self.client.logout()

        self.client.login(username='Test2',password='Test2 pw')

        setattr(settings, 'ALLOW_STAFF_TO_HIJACKUSER', True)
        response = self.client.get('/hijack/1/', )
        print(response.status_code)
        if VERSION >= (1,7):
            self.assertEqual(response.status_code, 302)
        else:
            self.assertTrue('name="this_is_the_login_form"' in  str(response.content))
        
    def test_hijack_admin(self):
        from hijack.admin import HijackUserAdmin

        ua = HijackUserAdmin(User, AdminSite())
        self.assertEqual(ua.list_display, ('username', 'email', 'first_name', 'last_name',  'last_login', 'date_joined', 'is_staff', 'hijack_field',))


#    def test_hijack_







