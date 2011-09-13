from django.db import models
from bhp_common.models import MyBasicUuidModel
from lab_clinic_api.choices import REVIEW_STATUS
from lab import Lab

class Review(MyBasicUuidModel):

    lab = models.ForeignKey(Lab)

    review_status = models.CharField(
        max_length = 25,
        choices = REVIEW_STATUS,
        default = 'NOT_REVIEWED',
        )

    review_datetime = models.DateTimeField(        
        blank = True,
        null = True
        )

    class Meta:
        
        app_label = 'lab_clinic_api'
