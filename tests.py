from datetime import datetime
from django.utils import unittest
from bhp_common.utils import get_ip_address, get_iface_list
from lab_barcode.classes import Label
from lab_barcode.models import ZplTemplate, LabelPrinter, Client

"""
from django.utils import unittest
from lab_barcode.tests import LabelTestCase
suite = unittest.TestLoader().loadTestsFromTestCase(LabelTestCase)
unittest.TextTestRunner(verbosity=2).run(suite)
"""

class LabelTestCase(unittest.TestCase):

    def setUp(self):

        self.test_template_template = '^XA\n\
^FO250,25^BY2\n\
^BCN,50,Y,N,N\n\
^FD%(requisition_identifier)s^FS\n\
^FO250,75^BY2\n\
^FO530,25^ADN,18,10^FD%(protocol)s^FS\n\
^FO530,50^ADN,22,12^FD%(site)s^FS\n\
^FO530,75^ADN,22,12^FD%(aliquot_type)s^FS\n\
^FO530,100^ADN,22,12^FD%(item_count)s/%(item_count_total)s^FS\n\
^FO250,100^ACN,18,10^FD%(protocol)s ^AAN,18,10^FD%(panel)s^FS\n\
^FO250,120^ADN,18,10^FDPat: %(subject_identifier)s (%(initials)s)^FS\n\
^FO250,140^ADN,18,10^FDDOB: %(dob)s %(gender)s MayStore:%(may_store_samples)s^FS\n\
^FO250,160^ADN,18,10^FDDrawn: %(drawn_datetime)s^FS\n\
^XZ'

        # create a lable template 
        ZplTemplate.objects.filter(name='test_label').delete()
        ZplTemplate.objects.create(
            name = 'test_label',
            template = self.test_template_template,
            default = True
            )
            
        LabelPrinter.objects.filter(cups_printer_name='test_printer').delete()
        label_printer = LabelPrinter(
            cups_printer_name = 'test_printer',
            cups_server_ip = '192.168.157.2',
            default = False,
        )            
        label_printer.save()


        LabelPrinter.objects.filter(cups_printer_name='default_test_printer').delete()
        LabelPrinter.objects.create(
            cups_printer_name = 'default_test_printer',
            cups_server_ip = '192.168.157.10',
            default = True,
        )            
        
        Client.objects.filter(name='test_client').delete()        
        Client.objects.create(
            ip = '192.168.157.2',
            name = 'test_client',
            label_printer = label_printer,
            )    
                
    def testSetTemplate(self):

        # default template or top
        self.zpl_template = ZplTemplate.objects.filter(default=True)
        if not self.zpl_template:
            error_occured = True
            self.assertTrue(error_occured)
        # template by name
        self.zpl_template = ZplTemplate.objects.filter(name='test_label')
        if not self.zpl_template:
            error_occured = True
            self.assertTrue(error_occured)
        self.assertEqual(self.zpl_template[0].template, self.test_template_template)                              

    def testLabel(self):

        self.zpl_template = ZplTemplate.objects.get(name='test_label')

        # set label with no values other that template
        self.label = Label(template=self.zpl_template, client_ip='192.168.157.2')    
        
        self.label.set_label()
        self.assertEqual(self.label, self.zpl_template[0].template)
        self.assertEqual(self.label_formatted, self.zpl_template.template)          

        self.label.label_to_file()
        self.label.set_label_printer()        
        self.assertEqual(self.label.label_printer.cups_server_ip, '192.168.157.2')             

