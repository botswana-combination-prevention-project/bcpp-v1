from django.db import models
from lab_receive.models import BaseReceive
from bhp_registration.models import RegisteredSubject


class Receive(BaseReceive):

    registered_subject = models.ForeignKey(RegisteredSubject, null=True)

    objects = models.Manager()

    def __unicode__(self):
        return '%s' % (self.receive_identifier)

    class Meta:
        app_label = 'lab_clinic_api'
        #ordering =['result_identifier']
