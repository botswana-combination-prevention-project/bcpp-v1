from django.db import models
from bhp_common.models import MyBasicUuidModel

class GroupingHint (MyBasicUuidModel):

    """A model to refer to when the 'option' or 'choice' field name (related_to_field_name) of the foreignkey is not obvious, e.g. not = 'name'.  """

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
    
    def __unicode__(self):
        return '%s__%s' % (self.model_name, self.field_name)
        
    class Meta:
        app_label = "bhp_describer"
        unique_together = ['app_label', 'model_name', 'field_name']
                
