from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.lab.lab_requisition.models import BaseRequisition
from edc.map.classes import site_mappers

from apps.bcpp.choices import COMMUNITIES
from apps.bcpp_inspector.classes import InspectorMixin
from apps.bcpp_subject.models import SubjectVisit

from ..managers import RequisitionManager

from .aliquot_type import AliquotType
from .packing_list import PackingList
from .panel import Panel


class SubjectRequisition(InspectorMixin, BaseRequisition):

    subject_visit = models.ForeignKey(SubjectVisit)

    packing_list = models.ForeignKey(PackingList, null=True, blank=True)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    entry_meta_data_manager = RequisitionManager(SubjectVisit)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = self.get_visit().household_member.household_structure.household.plot.community
        super(SubjectRequisition, self).save(*args, **kwargs)

    def get_site_code(self):
        return site_mappers.get_current_mapper().map_code

    def get_visit(self):
        return self.subject_visit

    def aliquot(self):
        url = reverse('admin:bcpp_lab_aliquot_changelist')
        return """<a href="{url}?q={requisition_identifier}" />aliquot</a>""".format(url=url, requisition_identifier=self.requisition_identifier)
    aliquot.allow_tags = True

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Subject Requisition'
        unique_together = ('subject_visit', 'panel', 'is_drawn')
