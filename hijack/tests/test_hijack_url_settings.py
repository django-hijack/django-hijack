# -*- coding: utf-8 -*-
# Test cases for settings-dependent urls/decorators. Need to be run separately from HijackTests

from unittest import skipIf
import sys

from hijack import settings as hijack_settings
from hijack.tests.test_hijack import BaseHijackTests
from hijack.tests.utils import SettingsOverride


class AllowGetRequestsHijackTestCase(BaseHijackTests):

    def setUp(self):
        super(AllowGetRequestsHijackTestCase, self).setUp()

    def tearDown(self):
        super(AllowGetRequestsHijackTestCase, self).tearDown()

    @skipIf('AllowGetRequestsHijackTestCase' not in ' '.join(sys.argv),
            'Skipping test cases for settings-dependent urls/decorators which need to be run separately')
    def test_allow_get_requests(self):
        protected_urls = [
            '/hijack/{}/'.format(self.user.id),
            '/hijack/email/{}/'.format(self.user_email),
            '/hijack/username/{}/'.format(self.user_username),
            '/hijack/disable-hijack-warning/',
            '/hijack/release-hijack/',
        ]

        with SettingsOverride(hijack_settings, HIJACK_ALLOW_GET_REQUESTS=True):
            self.assertTrue(hijack_settings.HIJACK_ALLOW_GET_REQUESTS)
            for protected_url in protected_urls:
                self.assertNotEqual(self.client.get(protected_url, follow=True).status_code, 405,
                                    msg='GET requests should be allowed')


class CustomDecoratorHijackTestCase(BaseHijackTests):

    def setUp(self):
        super(CustomDecoratorHijackTestCase, self).setUp()

    def tearDown(self):
        super(CustomDecoratorHijackTestCase, self).tearDown()

    @skipIf('CustomDecoratorHijackTestCase' not in ' '.join(sys.argv),
            'Skipping test cases for settings-dependent urls/decorators which need to be run separately')
    def test_custom_decorator(self):
        custom_decorator_path = 'hijack.tests.test_app.decorators.no_decorator'
        with SettingsOverride(hijack_settings, HIJACK_DECORATOR=custom_decorator_path):
            self.assertEqual(hijack_settings.HIJACK_DECORATOR, custom_decorator_path)
            self.client.logout()
            self.client.login(username=self.user_username, password=self.user_password)
            response = self._hijack(self.staff_user)
            self.assertEqual(response.status_code, 403)
            self.assertNotIn('Log in', str(response.content))
