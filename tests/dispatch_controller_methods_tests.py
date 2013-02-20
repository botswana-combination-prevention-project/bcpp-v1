from datetime import datetime
from django.core.exceptions import ValidationError
from django.test import TestCase
from bhp_dispatch.classes import DispatchController


class DispatchControllerMethodsTests(TestCase):

    #fixtures = ['test_configuration.json']

    def init_test(self):

        dispatch_url = '/'
        dispatch_controller = DispatchController(
            'default', 'default', 'bhp_dispatch', 'test_item', 'test_item_identifier', dispatch_url)