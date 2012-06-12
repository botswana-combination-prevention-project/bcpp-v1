from django.db import models
from bhp_base_model.classes import BaseUuidModel
from bhp_base_model.fields import InitialsField
from lab_clinic_api.choices import REVIEW_STATUS
from lab import Lab

class Review(BaseUuidModel):

    lab = models.ForeignKey(Lab,
        editable = False
        )

    review_status = models.CharField(
        max_length = 25,
        choices = REVIEW_STATUS,
        default = 'REVIEWED',
        )
    
    comment = models.TextField(
        max_length = 50,
        blank = True,
        null = True
        )        

    clinician_initials = InitialsField()

    review_datetime = models.DateTimeField(        
        editable = False,
        blank = True,
        null = True
        )

    class Meta:
        
        app_label = 'lab_clinic_api'
