import socket, re
from datetime import date
from django.db import models
from django.conf import settings
from bhp_variables.models import StudySpecific
from bhp_identifier.classes import Identifier


class BaseRequisitionManager(models.Manager):

    def get_identifier(self, **kwargs):

        """Generate and return a locally unique requisition identifier"""        
        
        site_code = kwargs.get('site_code')        

        if not site_code:
            try:
                site_code = settings.SITE_CODE
            except AttributeError:
                raise AttributeError('Requisition needs a \'site_code\'. Got None. Either pass as a parameter or set SITE_CODE= in settings.py')

        if len(site_code) == 1:
            site_code = site_code + '0'
        
        return Identifier(subject_type = 'requisition', site_code = site_code).create()


    def get_identifier_for_device(self, **kwargs):

        """Generate and return a locally unique requisition identifier if created on a device / netbook"""        
        
        hostname = socket.gethostname()
        if re.match(r'[0-9]{2}', hostname[len(hostname)-2:]):
            device_id = hostname[len(hostname)-2:]
        else:
            device_id = StudySpecific.objects.all()[0].device_id    
        
        given_root_segment = str(device_id) + date.today().strftime('%m%d')
            
        return Identifier(subject_type = 'requisition').create_with_root(given_root_segment, counter_length=2)

