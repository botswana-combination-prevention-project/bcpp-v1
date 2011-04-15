from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_lab_registration.models import Patient
from bhp_research_protocol.models import Protocol

from bhp_lab_core.models import SpecimenType

""" 
    Lab receiving table.
    Create a LabReceive model in your app that inheret from this
    Add the patient key field, for example
    
"""
    
            
class Receive (MyBasicUuidModel):

    protocol = models.ForeignKey(Protocol)
    
    receive_identifier = models.CharField(
        verbose_name = 'Receiving Identifier',
        max_length = 25,
        null = True, 
        editable = False,
        )

    patient = models.ForeignKey(Patient)

    datetime_drawn = models.DateTimeField("Date and time drawn",
        validators=[
            datetime_not_future,]
            )
  
    datetime_received = models.DateTimeField("Date and time received",
        validators=[
            datetime_not_future,]
            )

    def __unicode__(self):
        return '%s %s' % (self.receive_identifier, self.patient)

    #def get_absolute_url(self):
    #    return "//labreceive/%s/" % self.id

    class Meta:
        app_label = 'bhp_lab_core'            
