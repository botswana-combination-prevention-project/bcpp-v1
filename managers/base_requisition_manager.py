import socket, re
from datetime import date, datetime
from django.db import models
from django.conf import settings
from django.contrib import messages
from bhp_variables.models import StudySpecific
from bhp_identifier.classes import Identifier
from lab_requisition.classes import ClinicRequisitionLabel


class BaseRequisitionManager(models.Manager):

    def get_identifier(self, **kwargs):

        """Generate and return a locally unique requisition identifier"""        
        
        site_code = kwargs.get('site_code')
        protocol_code = kwargs.get('protocol_code', '')                        

        if not site_code:
            try:
                site_code = settings.SITE_CODE
            except AttributeError:
                raise AttributeError('Requisition needs a \'site_code\'. Got None. Either pass as a parameter or set SITE_CODE= in settings.py')

        if len(site_code) == 1:
            site_code = site_code + '0'
        
        identifier = Identifier(subject_type = 'specimen', 
                            site_code = site_code, 
                            protocol_code = protocol_code,
                            counter_length = 4,
                            )
        identifier.create()
                                    
        return identifier                   


    def get_identifier_for_device(self, **kwargs):

        """Generate and return a locally unique requisition identifier if created on a device / netbook"""        

        # mostly will get device_id from hostname
        if kwargs.get('device_id'):
            device_id = kwargs.get('device_id')
        else:
            hostname = socket.gethostname()
            if re.match(r'[0-9]{2}', hostname[len(hostname)-2:]):
                device_id = hostname[len(hostname)-2:]
            else:
                device_id = StudySpecific.objects.all()[0].device_id    
        
        given_root_segment = str(device_id) + date.today().strftime('%m%d')
            
        return Identifier(subject_type = 'requisition').create_with_root(given_root_segment, counter_length=2)
        
    def print_label(self, **kwargs):
        
        requisition = kwargs.get('requisition')
        remote_addr = kwargs.get('remote_addr')
        if requisition.specimen_identifier:    
            for cnt in range(requisition.item_count_total, 0, -1):
                try:
                    label = ClinicRequisitionLabel(
                                            client_ip = remote_addr,
                                            item_count = cnt, 
                                            requisition = requisition,
                                            )
                    label.print_label()
                    requisition.is_labelled = True
                    requisition.modified = datetime.today()
                    requisition.save()                                             
                except ValueError, err:
                    raise ValueError('Unable to print, is the lab_barcode app configured?')
                    #messages.add_message(request, messages.ERROR, err)
                if not label.printer_error:
                    print_message = '%s for specimen %s at %s from host %s' % (label.message, requisition.requisition_identifier, datetime.today().strftime('%H:%M'), remote_addr)
                    li_class = "info"
                else:
                    print_message = '%s' % (label.message)
                    li_class = "error"
                    
        else:            
            print_message = "Label did not print."
            li_class = "error"            

