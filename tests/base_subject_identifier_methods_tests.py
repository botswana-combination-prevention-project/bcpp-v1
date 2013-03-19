from django.test import TestCase
from django.conf import settings
from bhp_identifier.classes import BaseSubjectIdentifier
from bhp_identifier.exceptions import CheckDigitError, IdentifierEncodingError, IdentifierDecodingError


class BaseSubjectIdentifierMethodsTests(TestCase):

    def test_p1(self):
        x = 0
        while x < 50:
            subject_identifier = BaseSubjectIdentifier()
            print subject_identifier.get_identifier()
            self.assertTrue(subject_identifier.get_identifier().startswith(settings.PROJECT_IDENTIFIER_PREFIX))
            self.assertTrue(subject_identifier.get_identifier().startswith(settings.PROJECT_IDENTIFIER_PREFIX + '-' + settings.DEVICE_ID))
            x += 1
