from django.db import models
from netbook import Netbook


class SvnHistory(models.Model):
    
    netbook = models.ForeignKey(Netbook)
    
    repo = models.CharField(
        max_length = 50,
        null = True,
        )
        
    last_revision_number = models.IntegerField(
        null = True,
        )        
        
    last_revision_date = models.CharField(
        max_length = 25,
        null = True,
        )
                
                
    class Meta:
        app_label = 'bhp_netbook'
                        
