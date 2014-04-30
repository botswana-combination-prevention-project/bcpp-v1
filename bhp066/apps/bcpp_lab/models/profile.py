from django.db import models

from edc.lab.lab_profile.models import BaseProfile

from ..managers import ProfileManager

from .aliquot_type import AliquotType


class Profile(BaseProfile):

    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name='Source aliquot type')

    objects = ProfileManager()

    def natural_key(self):
        return (self.name,)

    class Meta:
        app_label = 'bcpp_lab'
