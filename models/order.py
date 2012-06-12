from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.validators import datetime_not_future
from lab_aliquot.models import Aliquot
from lab_panel.models import Panel
from lab_order.managers import OrderManager


class Order(BaseUuidModel):

    order_identifier = models.CharField(
        verbose_name = 'Order number',
        max_length = 25,
        help_text = 'Allocated internally',
        db_index=True, 
        editable = False,               
        )

    order_datetime =  models.DateTimeField(
        verbose_name = 'Order Date',
        validators = [
            datetime_not_future,
        ],
        db_index=True,                
        )
    
    aliquot = models.ForeignKey(Aliquot)    
    
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
        return "/lab_order/order/%s/" % self.id   
    def get_search_url(self):
        return "/laboratory/order/search/order/byword/%s/" % self.id   

    class Meta:
        app_label = 'lab_order'    
        db_table = 'bhp_lab_core_order'
        

