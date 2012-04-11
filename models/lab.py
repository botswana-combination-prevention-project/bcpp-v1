from django.db import models
from bhp_common.models import MyBasicUuidModel
from lab_clinic_api.managers import LabManager

class Lab(MyBasicUuidModel):
   
    subject_identifier = models.CharField(
        max_length = 50,
        )

    protocol_identifier = models.CharField(
        max_length = 50,
        )
        
    clinician_initials = models.CharField(
        max_length = 3,
        )

    release_status = models.CharField( 
        max_length = 25, 
        blank = True,
        null = True
        )
    
    panel = models.CharField(
        max_length = 250,
        blank = True,
        null = True
        )

    drawn_datetime = models.DateTimeField(
        blank = True,
        null = True
        )

    receive_datetime = models.DateTimeField(
        blank = True,
        null = True
        )

    receive_identifier = models.CharField( 
        max_length = 25, 
        blank = True,
        null = True
        )

    aliquot_identifier = models.CharField( 
        max_length = 25, 
        blank = True,
        null = True
        )

    condition = models.CharField( 
        max_length = 250, 
        blank = True,
        null = True
        )
    
    order_identifier = models.CharField( 
        max_length = 25, 
        blank = True,
        null = True
        )
    order_datetime = models.DateTimeField(
        blank = True,
        null = True
        )

    result_identifier = models.CharField( 
        max_length = 25, 
        blank = True,
        null = True
        )
    
    release_datetime = models.DateTimeField(
        blank = True,
        null = True
        )

    objects = LabManager()
        
    def save(self, *args, **kwargs):
    
        # TODO: try to match to the local panel definition
    
        super(Lab,self).save(*args, **kwargs)
    
    def __unicode__(self):
        return '%s order %s for %s drawn %s [%s]' % (self.subject_identifier, self.order_identifier, self.panel, self.drawn_datetime.strftime('%Y-%m-%d'), self.release_status)

    class Meta:
        app_label = "lab_clinic_api"


