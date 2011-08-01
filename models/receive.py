from datetime import datetime
from django.db import models
from bhp_common.classes import LockableObject
from bhp_common.models import MyBasicUuidModel, MyBasicModel
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_common.fields import InitialsField
from bhp_lab_registration.models import Patient
from bhp_research_protocol.models import Protocol, Site
from bhp_lab_core.models import SpecimenType

""" 
    Lab receiving table.
    Create a LabReceive model in your app that inheret from this
    Add the patient key field, for example
    
"""

class ReceiveIdentifierTrackerManager(models.Manager):
    
    pass
    """
    @require_object_lock
    def create(self, **kwargs):
        return super(OrderIdentifierTrackerManager, self).create(kwargs)
    """    


class ReceiveIdentifierTracker(MyBasicModel, LockableObject):
    """
    A lockable model to create and track unique order numbers for new order records.
    """
    
    receive_identifier = models.CharField(
        verbose_name = 'Order number',
        max_length = 25,
        db_index=True,                
        )
    
    yyyymm = models.IntegerField(db_index=True,)
    
    # reset counter if yyyymm changes
    counter = models.IntegerField(db_index=True,)
   
    objects = OrderIdentifierTrackerManager()
    
    class Meta:
        app_label = 'bhp_lab_core'        
        ordering = ['yyyymm', 'counter']
        unique_together = ['yyyymm', 'counter']


class ReceiveManager(models.Manager):

    def get_identifier(self, **kwargs):
    
        yyyymm = datetime.now().strftime('%Y%m')
        
        last = ReceiveIdentifierTracker.objects.filter(yyyymm = yyyymm).order_by('-counter')

        if last:
            counter = last[0].counter + 1
            if counter >=100000:
                raise TypeError("ReceiveManager cannot receive more than 100,000 samples in a month")
        else:
            counter = 1
                
        receive_identifier = str(yyyymm) + str(counter).rjust(5,'0')

        ReceiveIdentifierTracker.objects.create(
            receive_identifier = receive_identifier,
            yyyymm = yyyymm,
            counter = counter,
            )
        
        return order_identifier

    def create_from_requisition(self, requisition_identifier):

        if Requisition.objects.filter(requisition_identifier = requisition_identifier, receive__isnull=True):
            requisition = Requisition.objects.get(requisition_identifier = requisition_identifier, receive__isnull=True)

            # create Receive
            super(ReceiveManager, self).create(
                
                )    
            
            # create Aliquot
            
            # create Order
        
     
class Receive (MyBasicUuidModel):

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
        app_label = 'bhp_lab_core'   
        verbose_name_plural='Receive'
