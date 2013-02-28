from django.test import TestCase
from bhp_identifier.classes import BaseSubjectIdentifier
from bhp_identifier.exceptions import CheckDigitError, IdentifierEncodingError, IdentifierDecodingError


class BaseSubjectIdentifierMethodsTests(TestCase):
    
    subject_identifier = BaseSubjectIdentifier()
    print subject_identifier.get_identifier()