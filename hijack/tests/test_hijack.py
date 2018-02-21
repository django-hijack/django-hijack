# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase, Client, RequestFactory
from django.contrib.auth.models import AnonymousUser

from compat import import_string, unquote_plus
from hijack import settings as hijack_settings
from hijack.helpers import is_authorized
from hijack.middleware import HijackRemoteUserMiddleware
from hijack.signals import hijack_started, hijack_ended
from hijack.templatetags.hijack_tags import can_hijack
from hijack.tests.utils import SettingsOverride

try:
    from django.urls import reverse
except ImportError:
    from django.core.urlresolvers import reverse


class BaseHijackTests(TestCase):

    def setUp(self):
        self.superuser_username = 'superuser'
        self.superuser_email = 'superuser@example.com'
        self.superuser_password = 'superuser_pw'
        self.superuser = User.objects.create_superuser(self.superuser_username, self.superuser_email, self.superuser_password)

        self.staff_user_username = 'staff_user'
        self.staff_user_email = 'staff_user@example.com'
        self.staff_user_password = 'staff_user_pw'
        self.staff_user = User.objects.create_user(self.staff_user_username, self.staff_user_email, self.staff_user_password)
        self.staff_user.is_staff = True
        self.staff_user.save()

        self.user_username = 'user'
        self.user_email = 'user@example.com'
        self.user_password = 'user_pw'
        self.user = User.objects.create_user(self.user_username, self.user_email, self.user_password)

        self.client.login(username=self.superuser_username, password=self.superuser_password)

    def tearDown(self):
        self.client.logout()

    def _hijack(self, user):
        return self.client.post('/hijack/%d/' % user.id, follow=True)

    def _release_hijack(self):
        response = self.client.post('/hijack/release-hijack/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('hijacked-warning' in str(response.content))
        return response


class HijackTests(BaseHijackTests):

    def setUp(self):
        super(HijackTests, self).setUp()

    def tearDown(self):
        super(HijackTests, self).tearDown()

    def test_basic_hijack(self):
        client = Client()
        client.login(username=self.superuser_username, password=self.superuser_password)
        hijacked_response = client.post('/hijack/%d/' % self.user.id, follow=True)
        self.assertEqual(hijacked_response.status_code, 200)
        hijack_released_response = client.post('/hijack/release-hijack/', follow=True)
        self.assertEqual(hijack_released_response.status_code, 200)
        client.logout()

    def assertHijackSuccess(self, response):
        self.assertEqual(response.status_code, 200)
        self.assertTrue(self.client.session['is_hijacked_user'])
        self.assertTrue('hijacked-warning' in str(response.content))
        self.assertFalse('Log in' in str(response.content))

    def assertHijackPermissionDenied(self, response):
        self.assertEqual(response.status_code, 403)
        self.assertFalse(getattr(self.client.session, 'is_hijacked_user', False))
        self.assertFalse('hijacked-warning' in str(response.content))

    def test_hijack_urls(self):
        self.assertEqual('/hijack/disable-hijack-warning/', reverse('hijack:disable_hijack_warning'))
        self.assertEqual('/hijack/release-hijack/', reverse('hijack:release_hijack'))
        self.assertEqual('/hijack/1/', reverse('hijack:login_with_id', args=[1]))
        self.assertEqual('/hijack/2/', reverse('hijack:login_with_id', kwargs={'user_id': 2}))
        self.assertEqual('/hijack/username/bob/', reverse('hijack:login_with_username', args=['bob']))
        self.assertEqual('/hijack/username/bob_too/', reverse('hijack:login_with_username', kwargs={'username': 'bob_too'}))
        self.assertEqual('/hijack/email/bob@bobsburgers.com/', unquote_plus(reverse('hijack:login_with_email', args=['bob@bobsburgers.com'])))
        self.assertEqual('/hijack/email/bob_too@bobsburgers.com/', unquote_plus(reverse('hijack:login_with_email', kwargs={'email': 'bob_too@bobsburgers.com'})))

    def test_hijack_url_user_id(self):
        response = self.client.post('/hijack/%d/' % self.user.id, follow=True)
        self.assertHijackSuccess(response)
        self._release_hijack()
        response = self.client.post('/hijack/%s/' % self.user.username, follow=True)
        self.assertEqual(response.status_code, 400)
        response = self.client.post('/hijack/-1/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_hijack_url_username(self):
        response = self.client.post('/hijack/username/%s/' % self.user_username, follow=True)
        self.assertHijackSuccess(response)
        self._release_hijack()
        response = self.client.post('/hijack/username/dfjakhdl/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_hijack_url_email(self):
        response = self.client.post('/hijack/email/%s/' % self.user_email, follow=True)
        self.assertHijackSuccess(response)
        self._release_hijack()
        response = self.client.post('/hijack/email/dfjak@hdl.com/', follow=True)
        self.assertEqual(response.status_code, 404)

    def test_hijack_permission_denied(self):
        self.client.logout()
        self.client.login(username=self.staff_user_username, password=self.staff_user_password)
        response = self._hijack(self.superuser)
        self.assertHijackPermissionDenied(response)
        response = self._hijack(self.staff_user)
        self.assertHijackPermissionDenied(response)
        response = self._hijack(self.user)
        self.assertHijackPermissionDenied(response)

    def test_release_before_hijack(self):
        response = self.client.post('/hijack/release-hijack/', follow=True)
        self.assertHijackPermissionDenied(response)

    def test_last_login_time_not_changed(self):
        self.client.logout()
        # user login to set user.last_login
        self.client.login(username=self.user_username, password=self.user_password)
        self.client.logout()
        user_last_login = User.objects.get(id=self.user.id).last_login
        self.assertIsNotNone(user_last_login)
        # super-user login to hijack
        self.client.login(username=self.superuser_username, password=self.superuser_password)
        su_last_login = User.objects.get(id=self.superuser.id).last_login
        self.assertIsNotNone(su_last_login)
        # this shall not update user last_login
        response = self._hijack(self.user)
        self.assertHijackSuccess(response)
        # this shall not update super-user last_login
        self._release_hijack()
        self.assertEqual(User.objects.get(id=self.user.id).last_login, user_last_login)
        self.assertEqual(User.objects.get(id=self.superuser.id).last_login, su_last_login)

    def test_disable_hijack_warning(self):
        response = self._hijack(self.user)
        self.assertTrue('hijacked-warning' in str(response.content))
        self.assertTrue(self.client.session['is_hijacked_user'])
        self.assertTrue(self.client.session['display_hijack_warning'])

        response = self.client.post('/hijack/disable-hijack-warning/?next=/hello/', follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse('hijacked-warning' in str(response.content))
        self.assertTrue(self.client.session['is_hijacked_user'])
        self.assertFalse(self.client.session['display_hijack_warning'])
        self._release_hijack()

    def test_permissions(self):
        self.assertTrue(self.superuser.is_superuser)
        self.assertTrue(self.superuser.is_staff)
        self.assertFalse(self.staff_user.is_superuser)
        self.assertTrue(self.staff_user.is_staff)
        self.assertFalse(self.user.is_superuser)
        self.assertFalse(self.user.is_staff)

    def test_settings(self):
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_DISPLAY_WARNING'))
        self.assertTrue(hijack_settings.HIJACK_DISPLAY_WARNING)
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_URL_ALLOWED_ATTRIBUTES'))
        self.assertEqual(hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES, ('user_id', 'email', 'username'))
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_AUTHORIZE_STAFF'))
        self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF)
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF'))
        self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF)
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_LOGIN_REDIRECT_URL'))
        self.assertEqual(hijack_settings.HIJACK_LOGIN_REDIRECT_URL, '/hello/')
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_LOGOUT_REDIRECT_URL'))
        self.assertEqual(hijack_settings.HIJACK_LOGOUT_REDIRECT_URL, '/hello/')
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_AUTHORIZATION_CHECK'))
        self.assertEqual(hijack_settings.HIJACK_AUTHORIZATION_CHECK, 'hijack.helpers.is_authorized_default')
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_DECORATOR'))
        self.assertEqual(hijack_settings.HIJACK_DECORATOR, 'django.contrib.admin.views.decorators.staff_member_required')
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_USE_BOOTSTRAP'))
        self.assertFalse(hijack_settings.HIJACK_USE_BOOTSTRAP)
        self.assertTrue(hasattr(hijack_settings, 'HIJACK_ALLOW_GET_REQUESTS'))
        self.assertFalse(hijack_settings.HIJACK_ALLOW_GET_REQUESTS)

    def test_settings_override(self):
        self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF)
        with SettingsOverride(hijack_settings, HIJACK_AUTHORIZE_STAFF=True):
            self.assertTrue(hijack_settings.HIJACK_AUTHORIZE_STAFF)
        self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF)

    def test_is_authorized(self):
        self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF)
        self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF)
        self.assertTrue(is_authorized(self.superuser, self.superuser))
        self.assertTrue(is_authorized(self.superuser, self.staff_user))
        self.assertTrue(is_authorized(self.superuser, self.user))
        self.assertFalse(is_authorized(self.staff_user, self.superuser))
        self.assertFalse(is_authorized(self.staff_user, self.staff_user))
        self.assertFalse(is_authorized(self.staff_user, self.user))
        self.assertFalse(is_authorized(self.user, self.superuser))
        self.assertFalse(is_authorized(self.user, self.staff_user))
        self.assertFalse(is_authorized(self.user, self.user))

    def test_is_authorized_staff_authorized(self):
        with SettingsOverride(hijack_settings, HIJACK_AUTHORIZE_STAFF=True):
            self.assertTrue(hijack_settings.HIJACK_AUTHORIZE_STAFF)
            self.assertFalse(hijack_settings.HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF)
            self.assertTrue(is_authorized(self.superuser, self.superuser))
            self.assertTrue(is_authorized(self.superuser, self.staff_user))
            self.assertTrue(is_authorized(self.superuser, self.user))
            self.assertFalse(is_authorized(self.staff_user, self.superuser))
            self.assertFalse(is_authorized(self.staff_user, self.staff_user))
            self.assertTrue(is_authorized(self.staff_user, self.user))
            self.assertFalse(is_authorized(self.user, self.superuser))
            self.assertFalse(is_authorized(self.user, self.staff_user))
            self.assertFalse(is_authorized(self.user, self.user))

    def test_is_authorized_staff_authorized_to_hijack_staff(self):
        with SettingsOverride(hijack_settings, HIJACK_AUTHORIZE_STAFF=True, HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF=True):
            self.assertTrue(hijack_settings.HIJACK_AUTHORIZE_STAFF)
            self.assertTrue(hijack_settings.HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF)
            self.assertTrue(is_authorized(self.superuser, self.superuser))
            self.assertTrue(is_authorized(self.superuser, self.staff_user))
            self.assertTrue(is_authorized(self.superuser, self.user))
            self.assertFalse(is_authorized(self.staff_user, self.superuser))
            self.assertTrue(is_authorized(self.staff_user, self.staff_user))
            self.assertTrue(is_authorized(self.staff_user, self.user))
            self.assertFalse(is_authorized(self.user, self.superuser))
            self.assertFalse(is_authorized(self.user, self.staff_user))
            self.assertFalse(is_authorized(self.user, self.user))

    def test_disallow_get_requests(self):
        self.assertFalse(hijack_settings.HIJACK_ALLOW_GET_REQUESTS)
        protected_urls = [
            '/hijack/{}/'.format(self.user.id),
            '/hijack/email/{}/'.format(self.user_email),
            '/hijack/username/{}/'.format(self.user_username),
            '/hijack/disable-hijack-warning/',
            '/hijack/release-hijack/',
        ]
        for protected_url in protected_urls:
            self.assertEqual(self.client.get(protected_url, follow=True).status_code, 405,
                             msg='GET requests should not be allowed')

    def test_notification_tag(self):
        response = self._hijack(self.user)
        self.assertHijackSuccess(response)
        response = self.client.get('/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Notification tag' in str(response.content))
        self.assertTrue('hijacked-warning' in str(response.content))

    def test_is_hijacked_filter(self):
        response = self._hijack(self.user)
        self.assertHijackSuccess(response)
        response = self.client.get('/hello/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'You are hijacking this user')

    def test_notification_filter(self):
        response = self._hijack(self.user)
        self.assertHijackSuccess(response)
        response = self.client.get('/hello/filter/')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('Notification filter' in str(response.content))
        self.assertTrue('hijacked-warning' in str(response.content))

    def test_bootstrap_option(self):
        with SettingsOverride(hijack_settings, HIJACK_USE_BOOTSTRAP=True):
            response = self._hijack(self.user)
            self.assertHijackSuccess(response)
            response = self.client.get('/hello/')
            self.assertTrue('hijacked-warning-bootstrap' in str(response.content))
            response = self.client.get('/hello/filter/')
            self.assertTrue('hijacked-warning-bootstrap' in str(response.content))

    def test_can_hijack_filter(self):
        self.assertTrue(can_hijack(self.superuser, self.staff_user))
        self.assertFalse(can_hijack(self.user, self.superuser))

    def test_custom_authorization_check(self):
        for custom_check_path in [
            'hijack.tests.test_app.authorization_checks.can_hijack_default',
            'hijack.tests.test_app.authorization_checks.everybody_can_hijack',
            'hijack.tests.test_app.authorization_checks.nobody_can_hijack',
        ]:
            with SettingsOverride(hijack_settings, HIJACK_AUTHORIZATION_CHECK=custom_check_path):
                custom_check = import_string(custom_check_path)
                for hijacker, hijacked in [
                        (self.superuser, self.superuser),
                        (self.superuser, self.staff_user),
                        (self.superuser, self.user),
                        (self.staff_user, self.superuser),
                        (self.staff_user, self.staff_user),
                        (self.staff_user, self.user),
                        (self.user, self.superuser),
                        (self.user, self.staff_user),
                        (self.user, self.user),
                ]:
                    self.assertEqual(custom_check(hijacker, hijacked), is_authorized(hijacker, hijacked))

    def test_default_decorator(self):
        self.client.logout()
        self.client.login(username=self.user_username, password=self.user_password)
        response = self._hijack(self.staff_user)
        self.assertEqual(response.status_code, 200)
        self.assertIn('Log in', str(response.content))

    def test_signals(self):
        received_signals = []

        def hijack_started_receiver(sender, hijacker_id, hijacked_id, request, hijacker, hijacked, **kwargs):
            self.assertEqual(hijacker_id, hijacker.id)
            self.assertEqual(hijacked_id, hijacked.id)
            received_signals.append('hijack_started_%d_%d' % (hijacker_id, hijacked_id))
        hijack_started.connect(hijack_started_receiver)

        def hijack_ended_receiver(sender, hijacker_id, hijacked_id, request, hijacker, hijacked, **kwargs):
            self.assertEqual(hijacker_id, hijacker.id)
            self.assertEqual(hijacked_id, hijacked.id)
            received_signals.append('hijack_ended_%d_%d' % (hijacker_id, hijacked_id))
        hijack_ended.connect(hijack_ended_receiver)

        self.assertEqual(len(received_signals), 0)
        self._hijack(self.user)
        self.assertEqual(len(received_signals), 1)
        self.assertIn('hijack_started_%d_%d' % (self.superuser.id, self.user.id), received_signals)
        self._release_hijack()
        self.assertEqual(len(received_signals), 2)
        self.assertIn('hijack_ended_%d_%d' % (self.superuser.id, self.user.id), received_signals)

    def test_custom_session_cookie_name(self):
        self.assertEqual(settings.SESSION_COOKIE_NAME, 'sessionid')
        with SettingsOverride(settings, SESSION_COOKIE_NAME='somethingelse'):
            self.client.login(username=self.superuser_username, password=self.superuser_password)
            response = self._hijack(self.user)
            self.assertHijackSuccess(response)
            self._release_hijack()

    def test_middleware_without_remote_user(self):
        middleware = HijackRemoteUserMiddleware()
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {}
        request.META = {}
        request.user = AnonymousUser()
        middleware.process_request(request)
        self.assertEqual(request.META.get('REMOTE_USER'), None)

    def test_middleware_with_remote_user(self):
        middleware = HijackRemoteUserMiddleware()
        factory = RequestFactory()
        request = factory.get('/')
        request.session = {'is_hijacked_user': True}
        request.META = {'REMOTE_USER': 'test_user'}
        request.user = self.superuser
        middleware.process_request(request)
        self.assertEqual(request.META.get('REMOTE_USER'), self.superuser_username)
