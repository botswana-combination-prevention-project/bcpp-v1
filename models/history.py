from django.db import models
from bhp_base_model.classes import BaseUuidModel


class History(BaseUuidModel):

    subject_identifier = models.CharField(max_length=25)

    test_code = models.CharField(max_length=25)

    value = models.CharField(max_length=25)

    drawn_datetime = models.DateTimeField()

    class Meta:
        app_label = 'lab_longitudinal'
