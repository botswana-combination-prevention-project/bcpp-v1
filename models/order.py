from datetime import datetime
from django.db import models
from django.db.models import Q
from bhp_variables.models import StudySpecific
from bhp_common.models import MyBasicUuidModel, MyBasicModel
from bhp_common.validators import datetime_not_future
from bhp_common.classes.locking import LockableObject,require_object_lock
from bhp_lab_core.models import Aliquot, Panel

class OrderIdentifierTrackerManager(models.Manager):
    
    pass
    """
    @require_object_lock
    def create(self, **kwargs):
        return super(OrderIdentifierTrackerManager, self).create(kwargs)
    """    


class OrderIdentifierTracker(MyBasicModel, LockableObject):
    """
    A lockable model to create and track unique order numbers for new order records.
    """
    
    order_identifier = models.CharField(
        verbose_name = 'Order number',
        max_length = 25,
        db_index=True,                
        )
    
    yyyymm = models.IntegerField(db_index=True,)
    
    # reset counter if yyyymm changes
    counter = models.IntegerField(db_index=True,)
   
    objects = OrderIdentifierTrackerManager()
    
    class Meta:
        app_label = 'bhp_lab_core'        
        ordering = ['yyyymm', 'counter']
        unique_together = ['yyyymm', 'counter']


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


class Order(MyBasicUuidModel):

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

    requisition = models.ForeignKey(Requisition)

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
        

