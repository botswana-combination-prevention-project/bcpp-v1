from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from apps.bcpp_subject.models import SubjectVisit

from ..models import BaseSubjectRequisition
from ..managers import RequisitionManager


class SubjectRequisition(BaseSubjectRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    entry_meta_data_manager = RequisitionManager(SubjectVisit)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = self.subject_visit.household_member.household_structure.household.plot.community
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(SubjectRequisition, self).save(*args, **kwargs)

    def get_visit(self):
        return self.subject_visit

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.subject_visit.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.subject_visit.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Lab Requisition'
        unique_together = ('subject_visit', 'panel', 'is_drawn')