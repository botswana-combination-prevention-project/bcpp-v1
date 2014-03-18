from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.lab.lab_requisition.models import BaseRequisition

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_clinic.models import ClinicVisit

from ..managers import ClinicRequisitionManager

from .clinic_packing_list import ClinicPackingList


class ClinicRequisition(BaseRequisition):

    clinic_visit = models.ForeignKey(ClinicVisit)

    packing_list = models.ForeignKey(ClinicPackingList, null=True, blank=True)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    history = AuditTrail()

    entry_meta_data_manager = ClinicRequisitionManager(ClinicVisit)

    def natural_key(self):
        return (self.requisition_identifier,)

    def get_visit(self):
        return self.clinic_visit

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.clinic_visit.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.clinic_visit.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        app_label = 'bcpp_clinic_lab'
        verbose_name = 'Patient Clinic Requisition'
