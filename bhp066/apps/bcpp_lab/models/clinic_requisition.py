from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.entry_meta_data.models import RequisitionMetaData, ScheduledEntryMetaData
from edc.lab.lab_requisition.models import BaseRequisition
from edc.subject.entry.models import LabEntry, Entry

from apps.bcpp_clinic.models import ClinicVisit
from apps.bcpp.choices import COMMUNITIES

from ..managers import ClinicRequisitionManager

from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel


class ClinicRequisition(BaseRequisition):

    clinic_visit = models.ForeignKey(ClinicVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    history = AuditTrail()

    entry_meta_data_manager = ClinicRequisitionManager(ClinicVisit)

    def natural_key(self):
        return (self.requisition_identifier,)

    def get_visit(self):
        return self.clinic_visit

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    def aliquot(self):
        url = reverse('admin:bcpp_lab_aliquot_changelist')
        return """<a href="{url}?q={requisition_identifier}" />aliquots</a>""".format(
            url=url, requisition_identifier=self.requisition_identifier)
    aliquot.allow_tags = True

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.clinic_visit.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.clinic_visit.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    def change_metadata_status_on_post_save(self, **kwargs):
        """Changes the viralloadresult metadata status to NEW only if VL requisition is KEYED."""
        lab_entry = LabEntry.objects.get(requisition_panel__name='Clinic Viral Load', app_label='bcpp_lab', model_name='clinicrequisition')
        requisition_meta_data = RequisitionMetaData.objects.filter(appointment=self.clinic_visit.appointment,
                                                                   lab_entry=lab_entry,
                                                                   registered_subject=self.clinic_visit.appointment.registered_subject)
        if requisition_meta_data:
            requisition_meta_data = RequisitionMetaData.objects.get(appointment=self.clinic_visit.appointment,
                                                                   lab_entry=lab_entry,
                                                                   registered_subject=self.clinic_visit.appointment.registered_subject)
            if requisition_meta_data.entry_status == 'KEYED':
                entry = Entry.objects.get(model_name='clinicvlresult', visit_definition_id=self.clinic_visit.appointment.visit_definition_id)
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(appointment=self.clinic_visit.appointment,
                                                                            entry=entry,
                                                                            registered_subject=self.clinic_visit.appointment.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(appointment=self.clinic_visit.appointment,
                                                                            entry=entry,
                                                                            registered_subject=self.clinic_visit.appointment.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = 'NEW'
                scheduled_meta_data.save()
                return scheduled_meta_data

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Clinic Requisition'