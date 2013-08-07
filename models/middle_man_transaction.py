from django.db import models
from django.db.models import get_model
from base_transaction import BaseTransaction
from django.conf import settings
from datetime import datetime
from bhp_sync.classes import TransactionProducer, DeserializeFromTransaction

class MiddleManTransaction(BaseTransaction):

    """ transactions produced locally to be consumed/sent to a queue or consumer """

    is_consumed_middleman = models.BooleanField(
        default=False,
        db_index=True,
        )
    
    is_consumed_server = models.BooleanField(
        default=False,
        db_index=True,
        )
    
    def save(self, *args, **kwargs):
        if self.is_consumed_server and not self.consumed_datetime:
            self.consumed_datetime = datetime.today()
        if not 'MIDDLE_MAN' in dir(settings) or not settings.MIDDLE_MAN:
            raise TypeError('\'{0}\' is not configured to be a MiddleMan, so you cannot save MiddleMan transanctions here.'.format(settings.DEVICE_ID))
        super(MiddleManTransaction, self).save(*args, **kwargs)
        
    def deserialize_to_inspector_on_post_save(self, **kwargs):
        model_dict = DeserializeFromTransaction().decrypt_transanction(self)[0]
        tokens = model_dict.get('model').split('.')
        app_name = tokens[0]
        model_name = tokens[1]
        model = get_model(app_name,model_name)
        if model and 'save_to_inspector' in dir(model):
            fields = model_dict.get('fields')
            model().save_to_inspector(fields)
            
    objects = models.Manager() 
    class Meta:
        app_label = 'bhp_sync'
        ordering = ['timestamp']