from django.db import models

from edc.lab.lab_profile.models import BaseProfileItem

from ..managers import ProfileItemManager

from .aliquot_type import AliquotType
from .profile import Profile


class ProfileItem(BaseProfileItem):

    profile = models.ForeignKey(Profile)

    aliquot_type = models.ForeignKey(AliquotType)

    objects = ProfileItemManager()

    def __unicode__(self):
        return unicode(self.aliquot_type)

    def natural_key(self):
        return self.profile.natural_key() + self.aliquot_type.natural_key()

    class Meta:
        app_label = 'bcpp_lab'
        unique_together = ('profile', 'aliquot_type')