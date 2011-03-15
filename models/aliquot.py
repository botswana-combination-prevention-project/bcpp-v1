from django.db import models
from bhp_common.models import MyBasicUuidModel, MyBasicListModel

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
    id_int = models.IntegerField(
        editable=False
        )
    id_seed = models.IntegerField(
        editable=False
        )
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        )
    aliquot_volume = models.DecimalField("Volume in mL / Spots",
        max_digits=10,decimal_places=2
        )
    aliquot_condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        )
    
    def __unicode__(self):
        return self.aliquot_identifier

    class Meta:
        app_label = 'bhp_lab'

  
