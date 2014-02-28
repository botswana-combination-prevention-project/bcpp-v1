from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from apps.bcpp_rbd_subject.models import SubjectVisitRBD

from ..models import BaseSubjectRequisition
from ..managers import RequisitionManager


class RBDSubjectRequisition(BaseSubjectRequisition):

    subject_visit_rbd = models.ForeignKey(SubjectVisitRBD)

    entry_meta_data_manager = RequisitionManager(SubjectVisitRBD)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = self.subject_visit_rbd.household_member.household_structure.household.plot.community
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(RBDSubjectRequisition, self).save(*args, **kwargs)

    def get_visit(self):
        return self.subject_visit_rbd

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.subject_visit_rbd.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.subject_visit_rbd.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Blood Draw Only Requisition'
