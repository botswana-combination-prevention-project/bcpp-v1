from django.db import models
from bhp_common.models import MyBasicListModel

class AliquotMedium(MyBasicListModel):

    def __unicode__(self):
        return "%s" % ( self.name.upper())
    class Meta:
        ordering = ["name"]
        app_label = 'lab_aliquot_list'
        db_table = 'bhp_lab_core_aliquotmedium' 
