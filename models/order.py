from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_future
from bhp_lab_core.models import Aliquot, Panel
from bhp_lab_core.managers import OrderManager

class Order(MyBasicUuidModel):

    order_identifier = models.CharField(
        verbose_name = 'Order number',
        max_length = 25,
        help_text = 'Allocated internally',
        db_index=True,                
        )

    order_datetime =  models.DateTimeField(
        verbose_name = 'Order Date',
        validators = [
            datetime_not_future,
        ],
        db_index=True,                
        )
    
    # allow blank/null so orders may be placed
    # before a sample is received.
    # This is the case if clinics place the order.
    aliquot = models.ForeignKey(Aliquot,
        blank = True,
        null = True,
        )    
    
    panel  = models.ForeignKey(Panel)

    comment = models.CharField(
        verbose_name = 'Comment',
        max_length = 150,
        null = True,
        blank = True,
        )
    
    dmis_reference = models.IntegerField(
        null=True,
        blank = True,        
        )
    
    objects = OrderManager()
    
    def __unicode__(self):
        return '%s %s' % (self.order_identifier, self.panel)
        
    def get_absolute_url(self):
        return "/bhp_lab_core/order/%s/" % self.id   
    def get_search_url(self):
        return "/laboratory/order/search/order/byword/%s/" % self.id   

    class Meta:
        app_label = 'bhp_lab_core'    
