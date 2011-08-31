import datetime
from django.db import models
from django.utils.translation import ugettext_lazy as _
from bhp_common.models import MyBasicUuidModel

class DmisImportHistory(MyBasicUuidModel):
    
    import_label = models.CharField(
        verbose_name = 'Import label',
        max_length=25,
        )
    
    import_datetime = models.DateTimeField(
        verbose_name = 'Last Import datetime',
        default = datetime.datetime.today()
  	    )
  
    def __unicode__(self):
        return '%s on %s' % (self.import_label, self.import_datetime)

    class Meta:
        app_label = 'bhp_lab_core' 
        db_table = 'bhp_lab_core_dmisimporthistory'
  	    
