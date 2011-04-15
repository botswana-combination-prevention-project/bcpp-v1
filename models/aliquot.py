from django.db import models
from bhp_common.models import MyBasicUuidModel, MyBasicListModel
from bhp_lab_core.choices import ALIQUOT_STATUS
from bhp_lab_core.choices import SPECIMEN_MEASURE_UNITS, SPECIMEN_MEDIUM
from bhp_lab_core.models import Receive

class AliquotType(MyBasicListModel):
    
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)

    class Meta:
        ordering = ["short_name"]
        app_label = 'bhp_lab_core'        
        
class AliquotCondition(MyBasicListModel):
    
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)
    class Meta:
        ordering = ["display_index"]
        app_label = 'bhp_lab_core'        


class Aliquot (MyBasicUuidModel):
    
    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier', 
        max_length=25, 
        unique=True, 
        help_text="Aliquot identifier", 
        editable=False
        )
    
    receive = models. ForeignKey(Receive)
        
    count = models.IntegerField(
        editable=False
        )
        
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        )
        
    medium  = models.CharField(
        verbose_name = 'Medium',
        max_length = 25,        
        choices = SPECIMEN_MEDIUM,
        default = 'tube',
        #help_text = "Indicate such as dbs card, tube, swab, etc",
        )
  
    measure  = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        )

    measure_units = models.CharField(
        max_length = 25,
        choices=SPECIMEN_MEASURE_UNITS,
        default = 'mL',
        )

        
    condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        )
        
    status = models.CharField(
        max_length = 25,
        choices = ALIQUOT_STATUS,
        default = 'available',
        )
    
    def __unicode__(self):
        return self.aliquot_identifier

    class Meta:
        app_label = 'bhp_lab_core'

  
