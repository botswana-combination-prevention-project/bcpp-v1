import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel

class DmisImportTransactionHistory(MyBasicUuidModel):
    
    transaction_type = models.CharField(
        verbose_name = 'Type',
        max_length=25,
        )
    
    identifier = models.CharField(
        verbose_name = 'Identifier',
        max_length=25,
        )

    import_datetime = models.DateTimeField(
        verbose_name = 'Last Import datetime',
        default = datetime.datetime.today()
  	    )
  
    def __unicode__(self):
        return '%s %s on %s' % (self.transaction_type, self.identifier, self.import_datetime)

    class Meta:
        app_label = 'lab_import_dmis' 
  	    
