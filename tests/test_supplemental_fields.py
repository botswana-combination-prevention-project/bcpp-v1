import numpy
from django.test import TestCase
from bhp_base_test.models import TestModel
from bhp_supplemental_fields.classes import SupplementalFields


class TestSupplementalFields(TestCase):

    def test_p1(self):
        sf = SupplementalFields(('f3', 'f4'), p=0.1)
        seq = sf._get_p_as_sequence()
        self.assertEqual(len(seq), 1000)
        self.assertEqual(seq.count(0), 100)
        self.assertEqual(seq.count(1), 900)

        sf = SupplementalFields(('f3', 'f4'), p=0.5)
        seq = sf._get_p_as_sequence()
        self.assertEqual(len(seq), 1000)
        self.assertEqual(seq.count(0), 500)
        self.assertEqual(seq.count(1), 500)

        sf = SupplementalFields(('f3', 'f4'), p=0.135)
        seq = sf._get_p_as_sequence()
        self.assertEqual(len(seq), 1000)
        self.assertEqual(seq.count(0), 135)
        self.assertEqual(seq.count(1), 865)

        self.assertRaises(AttributeError, SupplementalFields, "X", p=0.1)
        self.assertRaises(AttributeError, SupplementalFields, ('f3', 'f4'), p=1)
        self.assertRaises(AttributeError, SupplementalFields, ('f3', 'f4'), p=0.1355)

        P = 0
        INC = 1
        EXC = 2
        for opt in [(0.135, 135, 865), (0.5, 500, 500), (0.75, 750, 250)]:
            print 'p={0} include(0)={1} exclude(1)={2}'.format(*opt)
            sf = SupplementalFields(('f3', 'f4'), p=opt[P])
            self.assertEqual(sf._get_p_as_sequence().count(0), opt[INC])
            self.assertEqual(sf._get_p_as_sequence().count(1), opt[EXC])
            zero = []
            one = []
            for j in range(0, 1000):
                lst = []
                for i in range(0, 1000):
                    fields, exclude_fields = sf.choose_fields(('f1', 'f2', 'f3', 'f4', 'f5'), TestModel, None)
                    if fields == ('f1', 'f2', 'f3', 'f4', 'f5') and not exclude_fields:
                        lst.append(0)
                    elif fields == ('f1', 'f2', 'f5') and exclude_fields == ('f3', 'f4'):
                        lst.append(1)
                    else:
                        lst.append(2)
                        print '  fields={0}'.format(fields)
                        print '  exclude_fields={0}'.format(exclude_fields)
                zero.append(lst.count(0))
                one.append(lst.count(1))
                self.assertEqual(lst.count(2), 0)
                if opt[P] > 0.5:
                    self.assertTrue(lst.count(0) > lst.count(1))
                elif opt[P] < 0.5:
                    self.assertTrue(lst.count(0) < lst.count(1))
                else:
                    pass
                #print '    0 -> {0} < {1} < {2}'.format(opt[INC] - (opt[INC] * (opt[P] * 2)), lst.count(0), opt[INC] + (opt[INC] * (opt[P] * 2)))
                #self.assertTrue(opt[INC] - (opt[INC] * (opt[P] * 2)) < lst.count(0) < opt[INC] + (opt[INC] * (opt[P] * 2)))
                #print '    1 -> {0} < {1} < {2}'.format(opt[EXC] - (opt[EXC] * (opt[P] * 2)), lst.count(1), opt[EXC] + (opt[EXC] * (opt[P] * 2)))
                #self.assertTrue(opt[EXC] - (opt[EXC] * (opt[P] * 2)) < lst.count(1) < opt[EXC] + (opt[EXC] * (opt[P] * 2)))
                #self.assertTrue(lst.count(0) in range(110, 155), lst.count(0))
                #self.assertTrue(lst.count(1) in range(850, 883), lst.count(1))
            print '  Included mean={0} std={1}, n={2}'.format(numpy.mean(zero), numpy.std(zero), len(zero))
            print '  Excluded mean={0} std={1}, n={2} '.format(numpy.mean(one), numpy.std(one), len(one))
