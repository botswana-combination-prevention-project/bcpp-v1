from django.db import models

from edc.lab.lab_profile.models import BaseProfileItem

from .aliquot_type import AliquotType
from .profile import Profile


class ProfileItem(BaseProfileItem):

    profile = models.ForeignKey(Profile)

    aliquot_type = models.ForeignKey(AliquotType)

    def __unicode__(self):
        return unicode(self.aliquot_type)

    class Meta:
        app_label = 'bcpp_lab'
