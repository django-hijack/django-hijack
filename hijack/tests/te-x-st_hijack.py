from django.test import TestCase

from django.contrib.auth.models import User

from django.test.client import Client

class HijackTests(TestCase):
    def setUp(self):
        admin_user, _ = User.objects.get_or_create(pk=1, username='Admin', is_superuser=True)
        test1, _ = User.objects.get_or_create(pk=2, username='Test1')
        test2, _ = User.objects.get_or_create(pk=3, username='Test2')

        admin_user.set_password('Admin pw')
        test1.set_password('test1 pw')
        test2.set_password('test2 pw')

        admin_user.save()
        test1.save()
        test2.save()

        self.client = Client()


    def test_usersettings(self):
        admin = User.objects.get(pk=1)
        user = User.objects.get(pk=2)

        self.assertTrue(admin.is_superuser)
        self.assertFalse(user.is_superuser)


    def test_hijack(self):

        login = self.client.login(username='Admin', password='Admin pw')

        self.assertTrue(login)

        r = self.client.get('/hijack/2')

        print r.context

        self.assertFalse(True)
        
        """
        from django.test.client import Client
        c = Client()
        
        #resp = c.post('/admin/', {'username':'Admin','password':'Admin pw'})
        #print resp.status_code
        #print '-----______-----'
        c.login(username='Admin', password='Admin pw')
        resp = c.get('/hijack/2/')
        print resp.context['user']
        print resp.content
        print '-----______-----'

        resp = c.get('/admin/')
        print resp.context['user']
        print resp.status_code
        print '-----______-----'




        #rsp = c.login(username='Admin', password='Admin pw')
        #r = c.post('/admin/',{'username':'Admin','password':'Admin pw'})
        #r = c.get('/admin/auth/user/')
        #c.login(username='Admin', password='Admin pw')
        #print '-------________'
        #print r.content

        self.assertFalse(True)
        """


