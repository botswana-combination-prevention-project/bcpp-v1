from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel


class BaseAppendix(MyBasicUuidModel):
    
    code = models.CharField(
        max_length = 25,
        unique = True,
        )
    
    short_description = models.CharField(
        max_length = 300,
        )
        
    full_description = models.TextField(
        max_length = 600
        )        
        
    class Meta:
        abstract = True        
