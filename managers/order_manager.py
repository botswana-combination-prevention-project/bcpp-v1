from datetime import datetime
from django.db import models
from lab_order.models import OrderIdentifierTracker


class OrderManager(models.Manager):
    
    def get_identifier(self, **kwargs):
    
        yyyymm = datetime.now().strftime('%Y%m')
        
        last = OrderIdentifierTracker.objects.filter(yyyymm = yyyymm).order_by('-counter')

        if last:
            counter = last[0].counter + 1
        else:
            counter = 1
                
        order_identifier = str(yyyymm) + str(counter).rjust(4,'0')

        OrderIdentifierTracker.objects.create(
            order_identifier = order_identifier,
            yyyymm = yyyymm,
            counter = counter,
            )
        
        return order_identifier
