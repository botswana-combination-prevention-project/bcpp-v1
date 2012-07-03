#import socket, re
from datetime import date
from django.db import models
from bhp_variables.models import StudySpecific
from bhp_identifier.classes import Identifier
#from lab_requisition.classes import ClinicRequisitionLabel


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



        
        #    def print_label(self, **kwargs):
        #        
        #        requisition = kwargs.get('requisition')
        #        remote_addr = kwargs.get('remote_addr')
        #        cups_server_ip = kwargs.get('cups_server_ip')
        #        if requisition.specimen_identifier:    
        #            for cnt in range(requisition.item_count_total, 0, -1):
        #                try:
        #                    label = ClinicRequisitionLabel(
        #                                            client_ip = remote_addr,
        #                                            cups_server_ip = cups_server_ip,
        #                                            item_count = cnt, 
        #                                            requisition = requisition,
        #                                            )
        #                    label.print_label()
        #                    requisition.is_labelled = True
        #                    requisition.modified = datetime.today()
        #                    requisition.save()                                             
        #                except ValueError, err:
        #                    raise ValueError('Unable to print, is the lab_barcode app configured? %s' % (err,))

