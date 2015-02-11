from django.test import TestCase

from django.contrib.auth.models import User

from django.test.client import Client

class HijackTests(TestCase):

    def setUp(self):
        admin_user, _ = User.objects.get_or_create(pk=1, username='Admin', email='admin@test.ch', is_superuser=True, is_staff=True,)
        if _:
            admin_user.set_password('Admin pw')
            admin_user.save()
        test1, _ = User.objects.get_or_create(pk=2, username='Test1', email='user1@test.ch', is_staff=False)
        if _:
            test1.set_password('Test1 pw')
            test1.save()
        test2, _ = User.objects.get_or_create(pk=3, username='Test2', email='user2@test.ch', is_staff=True)
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
        response = self.client.get('/hijack/3/', follow=True)
        self.assertTrue('on behalf of %s' % response.context['user'].username in response.content)
        
        response = self.client.get('/hijack/release-hijack/', follow=True)
        self.assertEquals(response.context['user'].username, 'Admin')
        
        response = self.client.get('/hijack/2/', follow=True)
        self.assertTrue('on behalf of %s' % (response.context['user'].username) in response.content)
        
        response = self.client.get('/hijack/disable-hijack-warning/?next=/hello', follow=True)
        self.assertFalse('on behalf of %s' % (response.context['user'].username) in response.content)

        #self.client.login(username='Admin',password='Admin pw')
        #response = self.client.get('/hijack/3/', follow=True)
        #self.assertTrue('on behalf of %s' % (response.context['user'].username) in response.content)

    def test_hijack_email(self):
        self.client.login(username='Admin',password='Admin pw')
        response = self.client.get('/hijack/email/user2@test.ch/', follow=True)
        self.assertEquals(response.context['user'].username, 'Test2')

    def test_hijack_username(self):
        self.client.login(username='Admin',password='Admin pw')
        response = self.client.get('/hijack/username/Test1', follow=True)
        self.assertEquals(response.context['user'].username, 'Test1')
