from django.db import models
from bhp_base_model.classes import BaseUuidModel


class UpdateLog(BaseUuidModel):

    subject_identifier = models.CharField(
        max_length=25,
        )

    update_datetime = models.DateTimeField()

    objects = models.Manager()

    class Meta:

        app_label = 'lab_clinic_api'
