from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_lab_registration.models import Patient
from bhp_lab_core.choices import SPECIMEN_MEASURE_UNITS, SPECIMEN_MEDIUM
from bhp_lab_core.models import Aliquot, SpecimenType

""" 
    Lab receiving table.
    Create a LabReceive model in your app that inheret from this
    Add the patient key field, for example
    
"""
    
            
class Receive (MyBasicUuidModel):

    receive_identifier = models.CharField(
        verbose_name = 'Receiving Identifier',
        max_length = 25,
        null = True, 
        editable = False,
        )

    patient = models.ForeignKey(Patient)

    datetime_drawn = models.DateTimeField("Date and time drawn",
            validators=[
            datetime_not_before_study_start,
            datetime_not_future,]
            )

    specimen_type = models.ForeignKey(SpecimenType,
        verbose_name = 'Specimen type',
        )
    
    specimen_medium  = models.CharField(
        verbose_name = 'Medium',
        max_length = 25,        
        choices = SPECIMEN_MEDIUM,
        help_text = "Indicate such as dbs card, tube, swab, etc",
        )
  
    specimen_measure  = models.DecimalField(
        max_digits = 10,
        decimal_places = 2,
        )

    specimen_measure_units = models.CharField(
        max_length = 25,
        choices=SPECIMEN_MEASURE_UNITS,
        )
  
    datetime_received = models.DateTimeField("Date and time received",
        validators=[
            datetime_not_future,]
            )

    aliquot = models.ForeignKey(Aliquot)


    def __unicode__(self):
        return unicode(self.aliquot)

    #def get_absolute_url(self):
    #    return "//labreceive/%s/" % self.id

    class Meta:
        app_label = 'bhp_lab'            
