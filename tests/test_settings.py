"""Check environment configuration without starting Django or connecting to a DB."""

import os
from pathlib import Path
import runpy
import unittest
from unittest.mock import patch

from django.core.exceptions import ImproperlyConfigured


SETTINGS_PATH = Path(__file__).resolve().parents[1] / "config" / "settings.py"
TEST_SECRET = "test-only-secret-for-settings-checks"


def load_settings(**environment):
    # Host machine variables must not change which startup path a test checks.
    with patch.dict(os.environ, environment, clear=True):
        return runpy.run_path(str(SETTINGS_PATH))


class SettingsEnvironmentTests(unittest.TestCase):
    def test_local_defaults_remain_available(self):
        settings = load_settings()
        self.assertIs(settings["DEBUG"], True)
        self.assertTrue(settings["SECRET_KEY"])
        self.assertEqual(settings["ALLOWED_HOSTS"], ["*"])
        self.assertEqual(settings["CSRF_TRUSTED_ORIGINS"], [])
        self.assertEqual(settings["DATABASES"]["default"]["HOST"], "127.0.0.1")

    def test_production_rejects_missing_or_empty_secret(self):
        for debug in ("false", "0", "no", "off", " FALSE "):
            for secret in (None, ""):
                with self.subTest(debug=debug, secret=secret):
                    environment = {"DJANGO_DEBUG": debug}
                    if secret is not None:
                        environment["DJANGO_SECRET_KEY"] = secret
                    with self.assertRaisesRegex(ImproperlyConfigured, "DJANGO_SECRET_KEY"):
                        load_settings(**environment)

    def test_production_keeps_configured_secret_and_limits_default_hosts(self):
        settings = load_settings(DJANGO_DEBUG="false", DJANGO_SECRET_KEY=TEST_SECRET)
        self.assertIs(settings["DEBUG"], False)
        self.assertEqual(settings["SECRET_KEY"], TEST_SECRET)
        self.assertEqual(settings["ALLOWED_HOSTS"], ["localhost", "127.0.0.1"])

    def test_true_values_keep_development_mode(self):
        for debug in ("1", "true", "yes", "on", " TRUE "):
            with self.subTest(debug=debug):
                self.assertIs(load_settings(DJANGO_DEBUG=debug)["DEBUG"], True)

    def test_host_and_origin_lists_strip_whitespace_and_empty_items(self):
        settings = load_settings(
            DJANGO_DEBUG="false",
            DJANGO_SECRET_KEY=TEST_SECRET,
            DJANGO_ALLOWED_HOSTS=" example.com, ,www.example.com, ",
            DJANGO_CSRF_TRUSTED_ORIGINS=" https://example.com, ,https://www.example.com, ",
        )
        self.assertEqual(settings["ALLOWED_HOSTS"], ["example.com", "www.example.com"])
        self.assertEqual(
            settings["CSRF_TRUSTED_ORIGINS"],
            ["https://example.com", "https://www.example.com"],
        )

    def test_explicit_empty_lists_do_not_fall_back_to_wildcard(self):
        settings = load_settings(DJANGO_ALLOWED_HOSTS=" , ", DJANGO_CSRF_TRUSTED_ORIGINS="")
        self.assertEqual(settings["ALLOWED_HOSTS"], [])
        self.assertEqual(settings["CSRF_TRUSTED_ORIGINS"], [])

    def test_database_connection_uses_all_environment_overrides(self):
        settings = load_settings(
            POSTGRES_DB="test_database",
            POSTGRES_USER="test_user",
            POSTGRES_PASSWORD="test-only-password",
            POSTGRES_HOST="database.internal",
            POSTGRES_PORT="6543",
        )
        self.assertEqual(
            settings["DATABASES"]["default"],
            {
                "ENGINE": "django.db.backends.postgresql",
                "NAME": "test_database",
                "USER": "test_user",
                "PASSWORD": "test-only-password",
                "HOST": "database.internal",
                "PORT": "6543",
            },
        )

    def test_explicit_secret_is_kept_in_development(self):
        self.assertEqual(load_settings(DJANGO_SECRET_KEY=TEST_SECRET)["SECRET_KEY"], TEST_SECRET)


if __name__ == "__main__":
    unittest.main()
