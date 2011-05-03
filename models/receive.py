from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_lab_registration.models import Patient
from bhp_research_protocol.models import Protocol, Site

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
  
    receive_datetime = models.DateTimeField("Date and time received",
        validators=[
            datetime_not_future,]
            )

    site = models.ForeignKey(Site)

    visit = models.CharField(
        verbose_name = "Visit",
        max_length=25,
        )
            
    dmis_reference = models.IntegerField()
    
    def __unicode__(self):
        return '%s' % (self.receive_identifier)

    def get_absolute_url(self):
        return "/bhp_lab_core/receive/%s/" % self.id   

    class Meta:
        app_label = 'bhp_lab_core'   
        verbose_name_plural='Receive'
