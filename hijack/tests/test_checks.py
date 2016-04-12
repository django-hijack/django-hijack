# -*- coding: utf-8 -*-
import django

if django.VERSION < (1, 7):
    pass
else:
    from django.conf import settings
    from django.core.checks import Error, Warning
    from django.test import TestCase

    from hijack import checks
    from hijack import settings as hijack_settings
    from hijack.apps import HijackConfig
    from hijack.tests.utils import SettingsOverride


    class ChecksTests(TestCase):

        def test_check_legacy_settings(self):
            with SettingsOverride(settings, ALLOW_STAFF_TO_HIJACKUSER=True):
                warnings = checks.check_legacy_settings(HijackConfig)
                expected_warnings = [
                    Warning(
                        'Deprecation warning: Setting "ALLOW_STAFF_TO_HIJACKUSER" has been renamed to "HIJACK_AUTHORIZE_STAFF"',
                        hint=None,
                        obj=None,
                        id='hijack.W002'
                    )
                ]
                self.assertEqual(warnings, expected_warnings)

        def test_check_url_allowed_attributes(self):
            errors = checks.check_url_allowed_attributes(HijackConfig)
            self.assertFalse(errors)

            with SettingsOverride(hijack_settings, HIJACK_URL_ALLOWED_ATTRIBUTES=('username',)):
                errors = checks.check_url_allowed_attributes(HijackConfig)
                self.assertFalse(errors)

            with SettingsOverride(hijack_settings, HIJACK_URL_ALLOWED_ATTRIBUTES=('username', 'email')):
                errors = checks.check_url_allowed_attributes(HijackConfig)
                self.assertFalse(errors)

            with SettingsOverride(hijack_settings, HIJACK_URL_ALLOWED_ATTRIBUTES=('other',)):
                errors = checks.check_url_allowed_attributes(HijackConfig)
                expected_errors = [
                    Error(
                        'Setting HIJACK_URL_ALLOWED_ATTRIBUTES needs to be '
                        'subset of (user_id, email, username)',
                        hint=None,
                        obj=hijack_settings.HIJACK_URL_ALLOWED_ATTRIBUTES,
                        id='hijack.E001',
                    )
                ]
                self.assertEqual(errors, expected_errors)

        def test_check_custom_authorization_check_importable(self):
            errors = checks.check_custom_authorization_check_importable(HijackConfig)
            self.assertFalse(errors)
            with SettingsOverride(hijack_settings, HIJACK_AUTHORIZATION_CHECK='not.importable'):
                expected_errors = [
                    Error(
                        'Setting HIJACK_AUTHORIZATION_CHECK cannot be imported',
                        hint=None,
                        obj='not.importable',
                        id='hijack.E002',
                    )
                ]
                errors = checks.check_custom_authorization_check_importable(HijackConfig)
                self.assertEqual(errors, expected_errors)

        def test_hijack_decorator_importable(self):
            errors = checks.check_hijack_decorator_importable(HijackConfig)
            self.assertFalse(errors)
            with SettingsOverride(hijack_settings, HIJACK_DECORATOR='not.importable'):
                expected_errors = [
                    Error(
                        'Setting HIJACK_DECORATOR cannot be imported',
                        hint=None,
                        obj='not.importable',
                        id='hijack.E003',
                    )
                ]
                errors = checks.check_hijack_decorator_importable(HijackConfig)
                self.assertEqual(errors, expected_errors)

        def test_check_staff_authorization_settings(self):
            errors = checks.check_staff_authorization_settings(HijackConfig)
            self.assertFalse(errors)
            with SettingsOverride(hijack_settings, HIJACK_AUTHORIZE_STAFF=True):
                errors = checks.check_staff_authorization_settings(HijackConfig)
                self.assertFalse(errors)
            with SettingsOverride(hijack_settings, HIJACK_AUTHORIZE_STAFF=True, HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF=True):
                errors = checks.check_staff_authorization_settings(HijackConfig)
                self.assertFalse(errors)
            with SettingsOverride(hijack_settings, HIJACK_AUTHORIZE_STAFF=False, HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF=True):
                errors = checks.check_staff_authorization_settings(HijackConfig)
                expected_errors = [
                    Error(
                        'Setting HIJACK_AUTHORIZE_STAFF_TO_HIJACK_STAFF may not be True if HIJACK_AUTHORIZE_STAFF is False.',
                        hint=None,
                        obj=None,
                        id='hijack.E004',
                    )
                ]
                self.assertEqual(errors, expected_errors)