import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel
from lab_receive.models import Receive
from lab_aliquot_list.models import AliquotCondition, AliquotType
from lab_aliquot.managers import AliquotManager
from lab_aliquot.choices import ALIQUOT_STATUS, SPECIMEN_MEASURE_UNITS, SPECIMEN_MEDIUM
       


class Aliquot (MyBasicUuidModel):
    
    aliquot_identifier = models.CharField(
        verbose_name='Aliquot Identifier', 
        max_length=25, 
        unique=True, 
        help_text="Aliquot identifier", 
        editable=False,
        )
        
    aliquot_datetime = models.DateTimeField(
        verbose_name = "Date and time aliquot created",
        default = datetime.datetime.today(),
        )
    
    receive = models.ForeignKey(Receive)
        
    count = models.IntegerField(
        editable=False,
        null=True
        )
        
    parent_identifier = models.ForeignKey('self',
        to_field = 'aliquot_identifier',
        blank=True,
        null=True,
        )
    
    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        )
        
    medium  = models.CharField(
        verbose_name = 'Medium',
        max_length = 25,        
        choices = SPECIMEN_MEDIUM,
        default = 'TUBE',
        #help_text = "Indicate such as dbs card, tube, swab, etc",
        )
  
    original_measure  = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default = '5.00',
        )

    current_measure  = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        default = '5.00',
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
        
    comment = models.CharField(
        max_length = 50,
        null=True,
        blank=True,
        )
    
    objects = AliquotManager()

  
    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    def get_absolute_url(self):
        return "/lab_aliquot/aliquot/%s/" % self.id   
        
    def get_search_url(self):
        return "/laboratory/aliquot/search/aliquot/byword/%s/" % self.id   

    class Meta:
        app_label = 'lab_aliquot'
        db_table = 'bhp_lab_core_aliquot'

  
