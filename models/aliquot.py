from django.db import models
from lab_aliquot.models import BaseAliquot
from receive import Receive


class Aliquot(BaseAliquot):

    receive = models.ForeignKey(Receive)

    objects = models.Manager()

    def __unicode__(self):
        return '%s' % (self.aliquot_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
        #ordering =['result_identifier']
