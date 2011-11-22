from django.db import models
from django.conf import settings
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
        
        #identifier_length = 8
            
        return Identifier(subject_type = 'requisition', site_code=site_code).create()

