from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_future
from bhp_lab_core.models import Aliquot, Panel

class Order(MyBasicUuidModel):

    order_number = models.CharField(
        verbose_name = 'Order number',
        max_length = 25,
        help_text = 'Allocated internally',
        )

    order_datetime =  models.DateTimeField(
        verbose_name = 'Order Date',
        validators = [
            datetime_not_future,
        ],
        )
    
    aliquot = models.ForeignKey(Aliquot)    
    
    panel  = models.ForeignKey(Panel)
    
    comment = models.CharField(
        verbose_name = 'Comment',
        max_length = 150,
        null = True,
        blank = True,
        )
    
    def __unicode__(self):
        return '%s %s %s' % (self.order_number, self.panel, self.order_datetime)

    class Meta:
        app_label = 'bhp_lab_core'    
