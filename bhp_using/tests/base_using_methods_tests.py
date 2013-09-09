from django.test import TestCase
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from bhp_using.exceptions import UsingError, UsingSourceError, UsingDestinationError
from bhp_using.classes import BaseUsing


class BaseUsingMethodsTests(TestCase):

    def test_methods(self):
        using_source = 'default'
        using_destination = 'destination'
        # Base tests
        self.assertTrue('DEVICE_ID' in dir(settings), 'Settings attribute DEVICE_ID not found')
        # raise source and destination cannot be the same
        self.assertRaises(UsingError, BaseUsing, using_source, using_source)
        # assert if not provided, server_device_id defaults to 99
        self.assertEqual(BaseUsing(using_source, using_destination).server_device_id, '99')
        # source must be either server or default
        self.assertRaises(UsingSourceError, BaseUsing, 'not_default', using_source)
        # assert 'xdefault' is not accepted
        self.assertRaises(ImproperlyConfigured, BaseUsing(using_source, using_destination).is_valid_using, 'xdefault', 'source')
        # assert accepts server_device_id as None of using_source is default
        self.assertRaises(UsingSourceError, BaseUsing, using_source, using_destination, server_device_id=None)
        # id source is default, must be server = 99
        self.assertRaises(UsingSourceError, BaseUsing, using_source, using_destination, server_device_id='22')
        # assert server_device_id cannot be None if osource is not default
        self.assertRaises(UsingSourceError, BaseUsing, 'destination', 'dispatch_destination', server_device_id=None)
        # assert server_device_id cannot be None if osource is not default
        self.assertEqual(BaseUsing('server', 'dispatch_destination', server_device_id='22').server_device_id, '22')
        # assert destination cannot be server
        self.assertRaises(UsingDestinationError, BaseUsing, using_source, 'server')
