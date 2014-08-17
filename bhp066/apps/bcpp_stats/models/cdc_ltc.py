from django.db import models

from .base_cdc import BaseCdc


class CdcLtc(BaseCdc):

    subject_id = models.CharField(max_length=25, null=True)
    appointment_date = models.DateField(null=True)
    followup_appt_date = models.DateField(null=True)

    class Meta:
        app_label = 'bcpp_stats'
