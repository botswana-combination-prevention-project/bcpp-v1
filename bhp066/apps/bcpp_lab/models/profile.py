from django.db import models

from edc.lab.lab_profile.models import BaseProfile

from .aliquot_type import AliquotType


class Profile(BaseProfile):

    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name='Source aliquot type')

    class Meta:
        app_label = 'bcpp_lab'
