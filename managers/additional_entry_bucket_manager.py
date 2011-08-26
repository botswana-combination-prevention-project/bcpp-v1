from datetime import datetime
from django.db import models
from bhp_common.models import ContentTypeMap
from bhp_entry.managers import BaseEntryBucketManager


class AdditionalEntryBucketManager(BaseEntryBucketManager):

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
                    
    def update_status(self, **kwargs):
    
        self.registered_subject = kwargs.get('registered_subject')        
        if not self.registered_subject:
            raise AttributeError, 'AdditionalEntryBucketManager.update_status requires \'registered_subject\'. Got None'

        self.set_content_type_map(**kwargs)
        
        action = kwargs.get('action', 'add_change')
        comment = kwargs.get('comment', '----')

        if self.content_type_map and self.registered_subject:

            report_datetime = datetime.today()

            if super(AdditionalEntryBucketManager, self).filter(registered_subject = self.registered_subject, content_type_map = self.content_type_map):
                s = super(AdditionalEntryBucketManager, self).get(registered_subject = self.registered_subject, content_type_map = self.content_type_map)
                status = self.get_status(
                    action = action, 
                    report_datetime = report_datetime, 
                    entry_status = s.entry_status, 
                    entry_comment = comment
                    )
                s.report_datetime = status['report_datetime']
                s.entry_status = status['entry_status']
                s.entry_comment = status['entry_comment']                
                # clear close_datetime
                s.close_datetime = status['close_datetime']
                s.modified = datetime.today()
                # save
                s.save()

