from datetime import datetime
from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_common.validators import datetime_not_future
from bhp_common.fields import InitialsField
from bhp_research_protocol.models import Protocol, Site
from lab_patient.models import Patient
from lab_receive.managers import ReceiveManager
     
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

    drawn_datetime = models.DateTimeField("Date and time drawn",
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
    
    receive_condition = models.CharField(
        verbose_name = 'Condition of primary tube',
        max_length = 50,
        null=True,
        )        
            
    dmis_panel_name = models.CharField(
        verbose_name = 'Panel name on dmis receive record',
        max_length = 50,
        null=True,
        )

    dmis_reference = models.IntegerField()
    
    objects = ReceiveManager()
    
    def __unicode__(self):
        return '%s' % (self.receive_identifier)

    def get_absolute_url(self):
        return "/lab_receive/receive/%s/" % self.id   

    class Meta:
        app_label = 'lab_receive'   
        verbose_name_plural='Receive'
        db_table = 'bhp_lab_core_receive'
