from django.db import models
from bhp_common.models import MyBasicUuidModel


class Producer(MyBasicUuidModel):
    
    name = models.CharField(
        max_length = 25,
        )
        
    url = models.CharField(
        max_length = 64,
        )                
        
    is_active = models.BooleanField(
        default=True
        )
    
            
    class Meta:
        app_label = 'bhp_sync'   
        ordering = ['name']         
