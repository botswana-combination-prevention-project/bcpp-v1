from copy import deepcopy
from django.test import TestCase
from bhp_context.classes import BaseContext


class BaseContextTests(TestCase):

    def test_p1(self):
        context = BaseContext()
        print 'init as empty dictionary'
        self.assertEqual(context._items, {})
        print 'if nothing added, method get() equals the default'
        self.assertEqual(context.get(), context._get_default_items())
        print 'if something added, method get() not equal to default'
        context.add(**{'erik': 12345})
        self.assertNotEqual(context.get(), context._get_default_items())
        print 'if adding to returned of default dictionary does not change instance of default dictionary'
        dct = deepcopy(context._get_default_items())
        dct.update({'erik': 12345})
        self.assertEqual(context.get(), dct)
        print 'if adding using add(), changes instance dictionary, otherwise not.'
        context.add({'mike': 6789})
        dct = context.get()
        dct.update({'mike': 6789})
        self.assertEqual(context.get(), dct)
        context.add({'jason': 6789}, maduo='11111')
        dct = context.get()
        dct.update({'jason': 6789, 'maduo': '11111'})
        self.assertEqual(context.get(), dct)
        lst = context._get_default_items().keys()
        lst.extend(['erik', 'mike', 'jason', 'maduo'])
        lst.sort()
        self.assertEqual(sorted(context.get().keys()), sorted(lst))
        print 'if remove(), removes item from instance dictionary'
        context.remove('maduo')
        del dct['maduo']
        self.assertEqual(context.get(), dct)
