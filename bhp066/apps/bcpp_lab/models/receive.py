from django.core.urlresolvers import reverse
from django.db import models

from edc.subject.registration.models import RegisteredSubject

from lis.specimen.lab_receive.models import BaseReceive

# from .subject_requisition import SubjectRequisition


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

    def requisition(self):
        #requisition = SubjectRequisition.objects.get(requisition_identifier=self.requisition_identifier)
        url = reverse('admin:bcpp_lab_subjectrequisition_changelist')
        return '<a href="{0}?q={1}">{1}</a>'.format(url, self.requisition_identifier)
    requisition.allow_tags = True

    class Meta:
        app_label = 'bcpp_lab'
