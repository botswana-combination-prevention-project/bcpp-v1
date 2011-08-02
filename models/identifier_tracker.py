from django.db import models
#from bhp_common.classes import LockableObject
from bhp_common.models import MyBasicModel

class IdentifierTracker(MyBasicModel): #, LockableObject):

    """
    A lockable model to create and track unique order numbers for new order records.
    """
    
    identifier = models.CharField(
        max_length = 25,
        db_index=True,                
        )
    
    root_number = models.IntegerField(db_index=True)
    
    counter = models.IntegerField(db_index=True)
   
    class Meta:
        app_label = 'bhp_common'        
        ordering = ['root_number', 'counter']
        unique_together = ['root_number', 'counter']
