from django.core.urlresolvers import reverse
from django.db import models

from edc_constants.constants import NO, NEW, NOT_REQUIRED, KEYED, UNKEYED
from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.device.sync.models import BaseSyncUuidModel
from edc.entry_meta_data.models import RequisitionMetaData, ScheduledEntryMetaData
from edc.entry_meta_data.managers import RequisitionMetaDataManager
from edc.lab.lab_requisition.models import BaseRequisition
from edc_map.classes import site_mappers
from edc.subject.entry.models import LabEntry, Entry
from edc_base.audit_trail import AuditTrail

from bhp066.apps.bcpp_clinic.models import ClinicVisit
from bhp066.apps.bcpp.choices import COMMUNITIES

from ..managers import ClinicRequisitionManager

from .aliquot_type import AliquotType
from .panel import Panel


class ClinicRequisition(BaseRequisition, BaseDispatchSyncUuidModel, BaseSyncUuidModel):

    clinic_visit = models.ForeignKey(ClinicVisit)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    objects = ClinicRequisitionManager()

    history = AuditTrail()

    entry_meta_data_manager = RequisitionMetaDataManager(ClinicVisit)

    def save(self, *args, **kwargs):
        self.community = self.get_visit().household_member.household_structure.household.plot.community
        super(ClinicRequisition, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{0} {1}'.format(unicode(self.panel), self.requisition_identifier)

    def natural_key(self):
        return (self.requisition_identifier,)

    def get_site_code(self):
        return site_mappers.get(self.community).map_code

    def get_visit(self):
        return self.clinic_visit

    @property
    def registered_subject(self):
        return self.clinic_visit.appointment.registered_subject

    @property
    def visit_code(self):
        return self.clinic_visit.appointment.visit_definition.code

    @property
    def optional_description(self):
        return ''

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    def aliquot(self):
        url = reverse('admin:bcpp_lab_aliquot_changelist')
        return """<a href="{url}?q={requisition_identifier}" />aliquots</a>""".format(
            url=url, requisition_identifier=self.requisition_identifier)
    aliquot.allow_tags = True

    def dashboard(self):
        url = reverse('clinic_dashboard_url',
                      kwargs={'dashboard_type': self.clinic_visit.appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.clinic_visit.appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    def change_metadata_status_on_post_save(self, **kwargs):
        """Changes the viralloadresult metadata status to NEW only if VL requisition is KEYED."""
        lab_entry = LabEntry.objects.get(
            requisition_panel__name='Clinic Viral Load',
            app_label='bcpp_lab', model_name='clinicrequisition')
        requisition_meta_data = RequisitionMetaData.objects.filter(
            appointment=self.clinic_visit.appointment,
            lab_entry=lab_entry,
            registered_subject=self.clinic_visit.appointment.registered_subject)
        if requisition_meta_data:
            requisition_meta_data = RequisitionMetaData.objects.get(
                appointment=self.clinic_visit.appointment,
                lab_entry=lab_entry,
                registered_subject=self.clinic_visit.appointment.registered_subject)
            if requisition_meta_data.entry_status == KEYED:
                entry = Entry.objects.get(
                    model_name='clinicvlresult',
                    visit_definition_id=self.clinic_visit.appointment.visit_definition_id)
                scheduled_meta_data = ScheduledEntryMetaData.objects.filter(
                    appointment=self.clinic_visit.appointment,
                    entry=entry,
                    registered_subject=self.clinic_visit.appointment.registered_subject)
                if not scheduled_meta_data:
                    scheduled_meta_data = ScheduledEntryMetaData.objects.create(
                        appointment=self.clinic_visit.appointment,
                        entry=entry,
                        registered_subject=self.clinic_visit.appointment.registered_subject)
                else:
                    scheduled_meta_data = scheduled_meta_data[0]
                scheduled_meta_data.entry_status = NEW
                scheduled_meta_data.save()
                return scheduled_meta_data

    def requisition_not_drawn(self):
            requisition = LabEntry.objects.get(
                requisition_panel__name='Clinic Viral Load', app_label='bcpp_lab', model_name='clinicrequisition')
            requisition_meta = RequisitionMetaData.objects.filter(
                appointment=self.clinic_visit.appointment,
                lab_entry=requisition,
                registered_subject=self.clinic_visit.appointment.registered_subject)
            if requisition_meta:
                requisition_meta = RequisitionMetaData.objects.get(
                    appointment=self.clinic_visit.appointment,
                    lab_entry=requisition,
                    registered_subject=self.clinic_visit.appointment.registered_subject)
                if requisition_meta.entry_status == KEYED:
                    if self.is_drawn == NO:
                        get_scheduled_form = 'clinicvlresult'
                        scheduled_entry = Entry.objects.filter(
                            model_name=get_scheduled_form,
                            visit_definition_id=self.clinic_visit.appointment.visit_definition_id)
                        scheduled_meta = ScheduledEntryMetaData.objects.filter(
                            appointment=self.clinic_visit.appointment,
                            entry=scheduled_entry,
                            registered_subject=self.clinic_visit.appointment.registered_subject)
                        for metadata in scheduled_meta:
                            if metadata.entry_status == UNKEYED:
                                metadata.entry_status = NOT_REQUIRED
                                metadata.save()

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Patient Clinic Requisition'
        unique_together = ('clinic_visit', 'panel', 'is_drawn')
