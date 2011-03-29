from django.db import models
from bhp_common.models import MyBasicUuidModel
from bhp_lab.models import Aliquot
from bhp_registration.models import RegisteredSubject
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
""" 
    Lab receiving table.
    Create a LabReceive model in your app that inheret from this
    Add the patient key field, for example
    
"""
    
            
class ReceiveModel (MyBasicUuidModel):
    aliquot = models.OneToOneField(Aliquot)
    
    datetime_received = models.DateTimeField("Date and time received",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future,]
            )
    datetime_drawn = models.DateTimeField("Date and time drawn",
            validators=[
            datetime_not_before_study_start,
            datetime_not_future,]
            )

    def __unicode__(self):
        return unicode(self.lab_aliquot)

    #def get_absolute_url(self):
    #    return "//labreceive/%s/" % self.id
    class Meta:
        abstract=True
        
class Receive(ReceiveModel):
    registered_subject = models.ForeignKey(RegisteredSubject,
    verbose_name="Subject",
    )
            
    class Meta:
        app_label = 'bhp_lab'            
