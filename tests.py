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

        self.test_cups_server_ip = '192.168.1.90'
        self.test_client_ip = '192.168.1.90'        
    
        # create a lable template 
        ZplTemplate.objects.filter(name='test_label').delete()
        ZplTemplate.objects.create(
            name = 'test_label',
            template = self.test_template_template,
            default = True
            )
            
        if LabelPrinter.objects.filter(cups_printer_name='test_printer'):
            LabelPrinter.objects.filter(cups_printer_name='test_printer').delete()
        label_printer = LabelPrinter(
            cups_printer_name = 'test_printer',
            cups_server_ip = self.test_cups_server_ip,
            default = False,
        )            
        label_printer.save()


        if LabelPrinter.objects.filter(cups_printer_name='default_test_printer'):
            LabelPrinter.objects.filter(cups_printer_name='default_test_printer').delete()
        LabelPrinter.objects.create(
            cups_printer_name = 'default_test_printer',
            cups_server_ip = '192.168.157.10',
            default = True,
            )            
        
        if Client.objects.filter(name='test_client'):
            Client.objects.filter(name='test_client').delete()        
        Client.objects.create(
            ip = self.test_client_ip,
            name = 'test_client',
            label_printer = label_printer,
            )    

        self.zpl_template = ZplTemplate.objects.get(name='test_label')
        
        
        # set label with no values other that template
        # self.label = Label(template=self.zpl_template, client_ip=self.test_client_ip) 
           
        self.label = Label(template=self.zpl_template, client_ip=self.test_client_ip)    
                
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

    def testSetClient(self):
        self.label.set_client()
        if self.label.client:
            self.assertEqual(self.label.client.ip, self.test_client_ip)             
        else:
            self.assertEqual(self.label.client_ip, self.test_client_ip)                             

    def testSetLabel(self):
        
        self.label.set_label()
        self.assertEqual(self.label.unformatted_label, self.zpl_template.template)
        self.assertEqual(self.label.formatted_label, self.zpl_template.template)          

    def testLabelToFile(self):

        self.label.label_to_file()
        self.assertRaises(self.label.file_name, None)             

        self.label.set_label_printer()        
        self.assertEqual(self.label.label_printer.cups_server_ip, self.test_cups_server_ip)  
    
    def testLabelPrinter(self):

        self.label.set_label_printer()
        self.assertRaises(self.label.label_printer, None)             
            
    def testCupsPrinterName(self):
        pass
                    
    def testPrintLabel(self):

        self.label.print_label()
        
                           
