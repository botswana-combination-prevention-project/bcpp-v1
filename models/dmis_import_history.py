import datetime
from django.db import models
from base_model import BaseModel


class DmisImportHistory(BaseModel):
    
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
        app_label = 'lab_import_dmis' 
