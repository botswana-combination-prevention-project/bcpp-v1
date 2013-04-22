from django.test import TestCase
from django.conf import settings
from bhp_identifier.classes import BaseSubjectIdentifier
from bhp_identifier.exceptions import CheckDigitError, IdentifierEncodingError, IdentifierDecodingError, IndentifierFormatError, IndentifierFormatKeyError


class BaseSubjectIdentifierMethodsTests(TestCase):

    def test_p1(self):
        site_code = '20'
        x = 0
        while x < 50:
            subject_identifier = BaseSubjectIdentifier(site_code=site_code)
            print subject_identifier.get_identifier()
            self.assertTrue(subject_identifier.get_identifier().startswith(settings.PROJECT_IDENTIFIER_PREFIX))
            self.assertTrue(subject_identifier.get_identifier().startswith('{0}-{1}{2}'.format(settings.PROJECT_IDENTIFIER_PREFIX, site_code, settings.DEVICE_ID)))
            x += 1

        print 'assert raises error if format has fewer keys that the values dictionary'
        subject_identifier = BaseSubjectIdentifier(identifier_format='{prefix}')
        self.assertRaises(IndentifierFormatError, subject_identifier.get_identifier)
        print 'assert raises error if format has more keys that the values dictionary'
        subject_identifier = BaseSubjectIdentifier(identifier_format='{identifier_prefix}-{site_code}{device_id}{sequence}{prefix}', site_code=site_code)
        self.assertRaises(IndentifierFormatError, subject_identifier.get_identifier)
        print 'assert raises error if get_identifier gets a value not in the format'
        subject_identifier = BaseSubjectIdentifier(identifier_format='{identifier_prefix}-{site_code}{device_id}{sequence}{prefix}', site_code=site_code)
        self.assertRaises(IndentifierFormatError, subject_identifier.get_identifier, erik=32)
