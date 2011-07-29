from datetime import datetime
from django.db import models
from django.db.models import Q
from bhp_variables.models import StudySpecific

class OrderManager(models.Manager):
    
    def get_identifier(self, **kwargs):
    
        order_identifier = datetime.now().strftime('%Y%m%d')
        
        return order_identifier
        

