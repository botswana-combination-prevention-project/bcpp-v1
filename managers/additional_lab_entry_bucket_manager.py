from datetime import datetime
from django.db import models
from bhp_entry.managers import BaseEntryBucketManager


class AdditionalLabEntryBucketManager(BaseEntryBucketManager):

    def add_for(self, registered_subject, requisition_model, qset):
        
        lab_entry = kwargs.get('lab_entry')
        if not self.requisition_instance:            
           
            if not super(AdditionalLabEntryBucketManager, self).filter(
                    registered_subject = registered_subject, 
                    panel = panel):            
                # add to bucket                                    
                super(AdditionalLabEntryBucketManager, self).create(
                    registered_subject = registered_subject,
                    lab_entry__panel = panel,
                    current_entry_title = model._meta.verbose_name,
                    fill_datetime = datetime.today(),
                    due_datetime = datetime.today(),                      
                    )
                    
    def update_status(self, **kwargs):
    
        self.registered_subject = kwargs.get('registered_subject')        
        if not self.registered_subject:
            raise AttributeError, 'AdditionalLabEntryBucketManager.update_status requires \'registered_subject\'. Got None'

        requisition_model = kwargs.get('requisition_model')        
        action = kwargs.get('action', 'add_change')
        comment = kwargs.get('comment', '----')
        # get the requisition_instance
        self.requisition_instance = requisition_model.objects.filter(qset)

        if self.requisition_instance and self.registered_subject:

            report_datetime = datetime.today()

            if super(AdditionalLabEntryBucketManager, self).filter(registered_subject = self.registered_subject, lab_entry__panel = self.requisition_instance.panel):
                s = super(AdditionalLabEntryBucketManager, self).get(registered_subject = self.registered_subject, lab_entry__panel = self.requisition_instance.panel)
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

