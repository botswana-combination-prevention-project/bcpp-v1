from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_common.fields import InitialsField
from bhp_research_protocol.models import Protocol, Site
from bhp_lab_patient.models import Patient
from bhp_lab_receive.managers import ReceiveManager
     
class Receive (MyBasicUuidModel):

    """ 
    Lab receiving table.
    Create a LabReceive model in your app that inheret from this
    Add the patient key field, for example
    """

    protocol = models.ForeignKey(Protocol)
    
    receive_identifier = models.CharField(
        verbose_name = 'Receiving Identifier',
        max_length = 25,
        null = True, 
        editable = False,
        db_index=True,                
        )
   
    patient = models.ForeignKey(Patient)

    datetime_drawn = models.DateTimeField("Date and time drawn",
        validators=[
            datetime_not_future,],
        db_index=True,                    
            )
  
    receive_datetime = models.DateTimeField(
        verbose_name = "Date and time received",
        default = datetime.now(),
        validators=[
            datetime_not_future,],
        db_index=True,                    
            )

    site = models.ForeignKey(Site)

    visit = models.CharField(
        verbose_name = "Visit Code",
        max_length=25,
        )
    
    clinician_initials = InitialsField()
            
    dmis_reference = models.IntegerField()
    
    objects = ReceiveManager()
    
    def __unicode__(self):
        return '%s' % (self.receive_identifier)

    def get_absolute_url(self):
        return "/bhp_lab_core/receive/%s/" % self.id   

    class Meta:
        app_label = 'bhp_lab_receive'   
        verbose_name_plural='Receive'
        db_table = 'bhp_lab_core_receive'
