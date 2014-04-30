from django.db import models

from edc.lab.lab_profile.models import BaseProfileItem

from .aliquot_type import AliquotType
from .aliquot_profile import AliquotProfile


class AliquotProfileItem(BaseProfileItem):

    profile = models.ForeignKey(AliquotProfile)

    aliquot_type = models.ForeignKey(AliquotType)

    def __unicode__(self):
        return unicode(self.aliquot_type)

    class Meta:
        app_label = 'bcpp_lab'
        db_table = 'bcpp_lab_profileitem'
