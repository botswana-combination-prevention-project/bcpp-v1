from django.db import models

from edc.lab.lab_profile.models import BaseProcessing

from .aliquot import Aliquot
from .aliquot_profile import AliquotProfile


class AliquotProcessing(BaseProcessing):

    aliquot = models.ForeignKey(Aliquot,
        verbose_name='Source Aliquot',
        help_text='Create aliquots from this one.')

    profile = models.ForeignKey(AliquotProfile,
        verbose_name='Profile',
        help_text='Create aliquots according to this profile.')

    class Meta:
        app_label = 'bcpp_lab'
        db_table = 'bcpp_lab_processing'
