from datetime import datetime

from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.device.device.classes import Device
from edc.lab.lab_requisition.models import BaseRequisition
from edc.map.classes import site_mappers

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_inspector.models import SubjectRequisitionInspector
from apps.bcpp_subject.models import SubjectVisit

from ..managers import SubjectRequisitionManager

from .packing_list import PackingList


class SubjectRequisition(BaseRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    history = AuditTrail()

    objects = SubjectRequisitionManager()

    def save(self, *args, **kwargs):
        self.community = self.household_member.household_structure.household.plot.community
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(SubjectRequisition, self).save(*args, **kwargs)

    def dispatch_container_lookup(self, using=None):
        return None

    def save_to_inspector(self, fields):
        if SubjectRequisitionInspector.objects.filter(subject_identifier=fields.get('subject_identifier'), requisition_identifier=fields.get('requisition_identifier')).count() == 0:
            device = Device()
            SubjectRequisitionInspector.objects.create(
                    subject_identifier=fields.get('subject_identifier'),
                    requisition_datetime=datetime.strptime(str(fields.get('requisition_datetime')).split('T')[0], '%Y-%m-%d'),  # FIXME: why strptime this??
                    requisition_identifier=fields.get('requisition_identifier'),
                    specimen_identifier=fields.get('specimen_identifier'),
                    device_id=device.get_device_id(),
                    app_name='bcpp_lab',
                    model_name='SubjectRequisition'
                    )

    def natural_key(self):
        return (self.requisition_identifier,)

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_visit(self):
        return self.subject_visit

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

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
