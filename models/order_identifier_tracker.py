#from django.db import models
#from bhp_base_model.classes import BaseModel
#
#
#class OrderIdentifierTracker(BaseModel):
#
#    """track unique order numbers for new order records."""
#    
#    order_identifier = models.CharField(
#        verbose_name = 'Order number',
#        max_length = 25,
#        db_index=True,                
#        )
#    
#    yyyymm = models.IntegerField(db_index=True,)
#    
#    # reset counter if yyyymm changes
#    counter = models.IntegerField(db_index=True,)
#   
#    class Meta:
#        app_label = 'lab_order'        
#        db_table = 'bhp_lab_core_orderidentifiertracker'
#        ordering = ['yyyymm', 'counter']
#        unique_together = ['yyyymm', 'counter']

