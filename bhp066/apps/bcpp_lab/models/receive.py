from django.db import models

from edc.subject.registration.models import RegisteredSubject

from lis.specimen.lab_receive.models import BaseReceive


class Receive(BaseReceive):

    registered_subject = models.ForeignKey(RegisteredSubject, null=True, related_name='bcpp_receive')

    requisition_model_name = models.CharField(max_length=25, null=True, editable=False)

    subject_type = models.CharField(max_length=25, null=True, editable=False)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_type = self.registered_subject.subject_type
        super(Receive, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.receive_identifier

    class Meta:
        app_label = 'bcpp_lab'
