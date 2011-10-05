from django.db import models
from bhp_common.models import MyBasicModel

class BaseCodeList (MyBasicModel):
    
    code = models.CharField("Code",
        max_length = 15,
        unique = True,
        )
    
    short_name = models.CharField("Name",
        max_length = 35,
        )    
    
    long_name = models.CharField("Long Name",
        max_length = 255,
        blank = True,
        )    
    def __unicode__(self):
        return "%s" % (self.short_name)
    class Meta:
        abstract = True
