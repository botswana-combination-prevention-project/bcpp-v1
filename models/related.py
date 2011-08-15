from django.db import models
from bhp_common.models import MyBasicUuidModel

class Related (MyBasicUuidModel):

    app_label =  models.CharField(
        max_length = 50,
        db_index = True
        )
    model_name = models.CharField(
        max_length = 50,
        db_index = True
        )

    field_name = models.CharField(
        max_length = 50,
        db_index = True
        )
    
    related_to_model = models.CharField(
        max_length = 50,
        )
    
    related_to_field_name = models.CharField(
        max_length = 50,
        )

    def __unicode__(self):
        return '%s__%s' % (self.model_name, self.field_name)
        
    class Meta:
        app_label = "bhp_describer"
        unique_together = ['app_label', 'model_name', 'field_name']
                
