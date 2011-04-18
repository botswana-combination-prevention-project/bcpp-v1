from django.db import models
from django.core.validators import RegexValidator
from bhp_common.models import MyBasicUuidModel, MyBasicListModel, MyBasicModel
from bhp_lab_core.choices import ALIQUOT_STATUS
from bhp_lab_core.choices import SPECIMEN_MEASURE_UNITS, SPECIMEN_MEDIUM
from bhp_lab_core.models import Receive

class AliquotType(MyBasicModel):

    name = models.CharField(
        verbose_name = 'Description',
        max_length=50,        
        )
    
    alpha_code = models.CharField(
        verbose_name = 'Aplha code',
        validators = [
            RegexValidator('^[A-Z]{2,15}$')
            ],
        max_length=15,
        )
    numeric_code = models.CharField(
        verbose_name = 'Numeric code (2-digit)',
        max_length = 2,
        validators = [
            RegexValidator('^[0-9]{2}$')
            ],
        )
        
    dmis_reference = models.IntegerField()        
    
    def __unicode__(self):
        return "%s: %s" % ( self.numeric_code, self.name.lower())

    class Meta:
        ordering = ["name"]
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
        editable=False,
        null=True
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
        default = 5.00,
        )

    measure_units = models.CharField(
        max_length = 25,
        choices=SPECIMEN_MEASURE_UNITS,
        default = 'mL',
        )

        
    condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        default = 10,
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

  
