from django.db import models

from edc.lab.lab_profile.models import BaseProcessing

from .aliquot import Aliquot
from .profile import Profile


class Processing(BaseProcessing):

    aliquot = models.ForeignKey(Aliquot,
        verbose_name='Source Aliquot',
        help_text='Create aliquots from this one.')

    profile = models.ForeignKey(Profile,
        verbose_name='Profile',
        help_text='Create aliquots according to this profile.')

    class Meta:
        app_label = 'bcpp_lab'
