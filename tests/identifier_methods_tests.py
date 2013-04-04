from django.test import TestCase
from bhp_identifier.classes import Identifier
from bhp_identifier.models import IdentifierTracker
from bhp_identifier.exceptions import CheckDigitError, IdentifierEncodingError, IdentifierDecodingError


class IdentifierMethodsTests(TestCase):

    def setUp(self):

        self.id = None
        if IdentifierTracker.objects.filter(identifier_string='123123123'):
            IdentifierTracker.objects.get(identifier_string='123123123').delete()

    def test_encoding(self):
        site_code = '10'
        mm = '02'
        yy = '13'
        IdentifierTracker.objects.all().delete()
        identifier = Identifier(identifier_type='subject', site_code=site_code, month=mm, year=yy)
        # check default for encode
        # check encode
        self.assertEqual(identifier.encode(123123123, 'base36', has_check_digit=False), '21AYER')
        self.assertEqual(identifier.decode('21AYER', 'base36', has_check_digit=False), 123123123)
        self.assertEqual(identifier.encode(123123125, 'base36', has_check_digit=False), '21AYET')
        self.assertEqual(identifier.decode('21AYET', 'base36', has_check_digit=False), 123123125)
        # assert same as above but it checked the checkdigit
        self.assertEqual(identifier.encode(123123125, 'base36', has_check_digit=True), '21AYET')
        self.assertEqual(identifier.decode('21AYET', 'base36', has_check_digit=True), 123123125)

        IdentifierTracker.objects.all().delete()
        identifier = Identifier(identifier_type='subject', site_code=site_code, counter_length=5, month=mm, year=yy)
        self.assertEqual(identifier.encode(123123123, 'base36', has_check_digit=False), '21AYER')
        IdentifierTracker.objects.all().delete()
        identifier = Identifier(identifier_type='subject', site_code=site_code, month=mm, year=yy)
        self.assertRaises(IdentifierEncodingError, identifier.encode, 123123123, 'erik', has_check_digit=False)
        self.assertRaises(CheckDigitError, identifier.encode, 123123123, 'base36')
        self.assertEqual(identifier.encode(123123125, 'base36'), '21AYET')
        self.assertRaises(IdentifierDecodingError, identifier.decode, '21AYET', 'erik', has_check_digit=False)
        self.assertRaises(CheckDigitError, identifier.decode, '21AYER', 'base36')
        self.assertEqual(identifier.decode('21AYET', 'base36'), 123123125)

    def test_create(self):
        site_code = '10'
        protocol_code = '041'
        mm = '02'
        yy = '13'
        IdentifierTracker.objects.all().delete()
        identifier = Identifier(identifier_type='subject', site_code=site_code, month=mm, year=yy)
        self.assertEqual(identifier.create(), '5Z7XC')
        self.assertEqual(IdentifierTracker.objects.all()[0].identifier, '5Z7XC')
        self.assertEqual(identifier.decode('5Z7XC', 'base36'), 10041312)
        self.assertEqual(identifier.create(), '5Z7XN')
        self.assertEqual(IdentifierTracker.objects.get(identifier='5Z7XN').identifier, '5Z7XN')
        identifier = Identifier(identifier_type='subject', site_code='20', protocol_code=protocol_code, month=mm, year=yy)
        self.assertEqual(identifier.create(), '97FX2FZ')
        self.assertEqual(IdentifierTracker.objects.get(identifier='97FX2FZ').identifier, '97FX2FZ')
        self.assertEqual(identifier.decode('97FX2FZ', 'base36'), 20041041311)
        self.assertEqual(identifier.create(), '97FX2GA')
        self.assertEqual(IdentifierTracker.objects.get(identifier='97FX2GA').identifier, '97FX2GA')
        self.assertEqual(identifier.decode('97FX2GA', 'base36'), 20041041322)
        print "assert raises error if root segment has a checkdigit that is invalid"
        self.assertRaises(CheckDigitError, identifier.create, root_segment='20041021313', has_check_digit=True)
        # assert that creating with a root segment encodes
        self.assertEqual(identifier.create(root_segment='20041021313', has_check_digit=False), '')

        # ...and decodes
        self.assertEqual(identifier.decode('PKO6NXBK', 'base36', has_check_digit=False), 2004102131312)

    def test_identifier_string(self):
        site_code = '10'
        protocol_code = '041'
        mm = '02'
        yy = '13'
        IdentifierTracker.objects.all().delete()
        identifier = Identifier(identifier_type='subject', month=mm, year=yy)
        self.assertEqual(identifier._get_identifier_string(), '1{0}{1}00'.format(mm, yy))
        IdentifierTracker.objects.all().delete()
        identifier = Identifier(identifier_type='subject', site_code=site_code, month=mm, year=yy)
        self.assertEqual(identifier._get_identifier_string(), '{0}{1}{2}03'.format(site_code, mm, yy))
        identifier = Identifier(identifier_type='subject', site_code=site_code, protocol_code=protocol_code, month=mm, year=yy)
        self.assertEqual(identifier._get_identifier_string(), '{0}{1}{2}{3}03'.format(site_code, protocol_code, mm, yy))
        identifier = Identifier(identifier_type='subject', site_code=site_code, protocol_code=protocol_code, month=mm, year=yy)
        self.assertEqual(identifier.create(), '4M25XMQ')
        self.assertEqual(identifier._get_identifier_string(), '10041021314')
        identifier.create()
        self.assertEqual(identifier._get_identifier_string(), '10041021325')
