import socket, re
from datetime import date, datetime
from django.db import models
from bhp_device.classes import Device
from bhp_variables.models import StudySpecific
from bhp_identifier.classes import Identifier
from lab_requisition.classes import ClinicRequisitionLabel


class BaseRequisitionManager(models.Manager):

    def get_global_identifier(self, **kwargs):

        """Generate and return a globally unique requisition identifier (adds site and protocolnumber)"""        
        
        if not StudySpecific.objects.all()[0].machine_type == 'SERVER':
            raise ValueError('Only SERVERs may access method \'get_global_identifier\'. \
                              Machine Type is determined from model StudySpecific attribute \
                              machine_type. Got %s' % (StudySpecific.objects.all()[0].machine_type, ))
        
        site_code = kwargs.get('site_code')
        protocol_code = kwargs.get('protocol_code', '')                        

        if not site_code:
            try:
                site_code = StudySpecific.objects.all()[0].site_code
            except AttributeError:
                raise AttributeError('Requisition needs a \'site_code\'. Got None. Either pass as a parameter or in StudySpecific')

        if len(site_code) == 1:
            site_code = site_code + '0'
            
        if not protocol_code:
            try:
                protocol_code = StudySpecific.objects.all()[0].protocol_code
            except AttributeError:
                raise AttributeError('Requisition needs a \'protocol_code\'. Got None. Either pass as a parameter or set in StudySpecific')
 
        
        identifier = Identifier(subject_type = 'specimen', 
                            site_code = site_code, 
                            protocol_code = protocol_code,
                            counter_length = 4,
                            )
        identifier.create()
                                    
        return identifier                   


    def get_identifier_for_device(self, **kwargs):

        """Generate and return a locally unique requisition identifier for a device (adds device id)"""        
        device = Device()
        if not device.device_id:
            raise ValueError('Device ID unknown. Must either be passed as a kwarg, extracted from hostname, or queried from StudySpecific.')    
        given_root_segment = str(device.device_id) + date.today().strftime('%m%d')
        
        return Identifier(subject_type = 'requisition').create_with_root(given_root_segment, 
                                                                         counter_length=2)
        
    def print_label(self, **kwargs):
        
        requisition = kwargs.get('requisition')
        remote_addr = kwargs.get('remote_addr')
        cups_server_ip = kwargs.get('cups_server_ip')
        if requisition.specimen_identifier:    
            for cnt in range(requisition.item_count_total, 0, -1):
                try:
                    label = ClinicRequisitionLabel(
                                            client_ip = remote_addr,
                                            cups_server_ip = cups_server_ip,
                                            item_count = cnt, 
                                            requisition = requisition,
                                            )
                    label.print_label()
                    requisition.is_labelled = True
                    requisition.modified = datetime.today()
                    requisition.save()                                             
                except ValueError, err:
                    raise ValueError('Unable to print, is the lab_barcode app configured? %s' % (err,))
                    #messages.add_message(request, messages.ERROR, err)
                #if not label.printer_error:
                #    print_message = '%s for specimen %s at %s from host %s' % (label.message, requisition.requisition_identifier, datetime.today().strftime('%H:%M'), remote_addr)
                ##    li_class = "info"
                #else:
                #    print_message = '%s' % (label.message)
                #    li_class = "error"
                    
        #else:            
        #    print_message = "Label did not print."
        #    li_class = "error"            

