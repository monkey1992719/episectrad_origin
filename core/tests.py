from unittest.mock import Mock, patch

from django.test import TestCase
from django.test import override_settings

import requests

from . import utils


class UtilsTests(TestCase):

    @override_settings(VALIDATE_EMAILS=True)
    @patch.object(requests, "get")
    def test_validate_email_success(self, mockget):
        mockresponce = Mock()
        mockresponce.json.return_value = {"address": "tokens@gmail.com",
                                          "did_you_mean": None,
                                          "is_disposable_address": False,
                                          "is_role_address": False,
                                          "is_valid": True,
                                          "mailbox_verification": None,
                                          "parts": {"display_name": None, "domain": "education-ecosystem.com",
                                                    "local_part": "tokens"}, "reason": None}
        mockresponce.status_code = 200
        mockget.return_value = mockresponce
        is_valid, info = utils.validate_email("tokens@gmail.com")
        self.assertTrue(is_valid)

    @override_settings(VALIDATE_EMAILS=True)
    @patch.object(requests, "get")
    def test_validate_email_failure(self, mockget):
        mockresponce = Mock()
        mockresponce.json.return_value = {"address": "tokensgmail.com",
                                          "did_you_mean": None,
                                          "is_disposable_address": False,
                                          "is_role_address": False,
                                          "is_valid": False,
                                          "mailbox_verification": None,
                                          "parts": {"display_name": None, "domain": "education-ecosystem.com",
                                                    "local_part": "tokens"}, "reason": None}
        mockresponce.status_code = 200
        mockget.return_value = mockresponce
        is_valid, info = utils.validate_email("tokensgail.com")
        self.assertFalse(is_valid)

    @override_settings(VALIDATE_EMAILS=True)
    @patch.object(requests, "get")
    def test_validate_email_hint(self, mockget):
        mockresponce = Mock()
        mockresponce.json.return_value = {"address": "tokens@gail.com",
                                          "did_you_mean": "tokens@gmail.com",
                                          "is_disposable_address": False,
                                          "is_role_address": False,
                                          "is_valid": True,
                                          "mailbox_verification": None,
                                          "parts": {"display_name": None, "domain": "education-ecosystem.com",
                                                    "local_part": "tokens"}, "reason": None}
        mockresponce.status_code = 200
        mockget.return_value = mockresponce
        is_valid, info = utils.validate_email("tokens@gail.com")
        self.assertTrue(is_valid)
        self.assertEqual(info, "Did you mean tokens@gmail.com?")
