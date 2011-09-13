from django.db import models
from bhp_common.models import MyBasicUuidModel

class UpdateLog(MyBasicUuidModel):

    subject_identifier = models.CharField(
        max_length = 25,
        )

    update_datetime = models.DateTimeField()

    class Meta:
        
        app_label = 'lab_clinic_api'
