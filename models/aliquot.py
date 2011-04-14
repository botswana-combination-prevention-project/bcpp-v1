from django.db import models
from bhp_common.models import MyBasicUuidModel, MyBasicListModel
from bhp_lab.choices import ALIQUOT_STATUS

class AliquotType(MyBasicListModel):
    
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)

    class Meta:
        ordering = ["short_name"]
        app_label = 'bhp_lab'        
        
class AliquotCondition(MyBasicListModel):
    
    def __unicode__(self):
        return "%s: %s" % ( self.short_name.upper() ,self.name)
    class Meta:
        ordering = ["display_index"]
        app_label = 'bhp_lab'        


class Aliquot (MyBasicUuidModel):
    
    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier', 
        max_length=25, 
        unique=True, 
        help_text="Aliquot identifier", 
        editable=False
        )
        
    count = models.IntegerField(
        editable=False
        )
        
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        )
        
    volume = models.DecimalField("Volume in mL / Spots",
        max_digits=10,
        decimal_places=2
        )
        
    condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        )
        
    status = models.CharField(
        max_length = 25,
        choices = ALIQUOT_STATUS,
        )
    
    def __unicode__(self):
        return self.aliquot_identifier

    class Meta:
        app_label = 'bhp_lab'

  
