from django.db import models
#from bhp_common.classes import LockableObject
from bhp_common.models import MyBasicModel

class IdentifierTracker(MyBasicModel): #, LockableObject):

    """
    A lockable model to create and track unique identifiers for new records such as requsitions, receive, etc.
    
    See also, classes/identifier.py
    
    """
    
    identifier = models.CharField(
        max_length = 25,
        db_index=True,                
        )
    
    identifier_string = models.CharField(
        max_length = 50,
        db_index=True,                
        )    
    
    root_number = models.IntegerField(db_index=True)
    
    counter = models.IntegerField(db_index=True)

    identifier_type = models.CharField(
        max_length = 35
        )
   
    class Meta:
        app_label = 'bhp_identifier'        
        ordering = ['root_number', 'counter']
        unique_together = ['root_number', 'counter']
