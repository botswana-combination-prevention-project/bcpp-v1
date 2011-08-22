from django.db import models
from bhp_common.models import ContentTypeMap

class AdditionalEntryBucketManager(models.Manager):

    def add_for(self, registered_subject, model, qset):
        
        # check that the form has been keyed already
        if not model.objects.filter(qset):            
            content_type_map = ContentTypeMap.objects.get(name = model._meta.verbose_name)
            
            if not super(AdditionalEntryBucketManager, self).filter(
                    registered_subject = registered_subject, 
                    content_type_map = content_type_map):            
                # add to bucket                                    
                super(AdditionalEntryBucketManager, self).create(
                    registered_subject = registered_subject,
                    content_type_map = content_type_map,
                    current_entry_title = model._meta.verbose_name,
                    fill_datetime = datetime.today(),
                    due_datetime = datetime.today(),                      
                    )
