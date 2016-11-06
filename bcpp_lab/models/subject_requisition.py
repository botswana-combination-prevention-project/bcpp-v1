from django.core.urlresolvers import reverse
from django.db import models

from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc_sync.model_mixins import SyncModelMixin
from edc_base.model.models import BaseUuidModel
from edc.entry_meta_data.managers import RequisitionMetaDataManager
from lab_requisition.models import RequisitionModelMixin
from edc_map.site_mappers import site_mappers
from edc_base.audit_trail import AuditTrail
from edc_constants.constants import YES, NO


from bhp066.apps.bcpp.choices import COMMUNITIES
from bhp066.apps.bcpp_inspector.classes import InspectorMixin
from bhp066.apps.bcpp_subject.constants import VIRAL_LOAD, POC_VIRAL_LOAD
from bhp066.apps.bcpp_subject.models import SubjectVisit

from ..managers import SubjectRequisitionManager

from .aliquot_type import AliquotType
from .panel import Panel


class SubjectRequisition(InspectorMixin, RequisitionModelMixin, BaseDispatchSyncUuidModel, SyncModelMixin, BaseUuidModel):

    subject_visit = models.ForeignKey(SubjectVisit)

    aliquot_type = models.ForeignKey(AliquotType)

    panel = models.ForeignKey(Panel)

    community = models.CharField(max_length=25, choices=COMMUNITIES, null=True, editable=False)

    objects = SubjectRequisitionManager()

    entry_meta_data_manager = RequisitionMetaDataManager(SubjectVisit)

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.community = self.get_visit().household_member.household_structure.household.plot.community
        super(SubjectRequisition, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{0} {1}'.format(unicode(self.panel), self.requisition_identifier)

    def get_site_code(self):
        return site_mappers.get_mapper(self.community).map_code

    def get_visit(self):
        return self.subject_visit

    @property
    def registered_subject(self):
        return self.subject_visit.appointment.registered_subject

    @property
    def visit_code(self):
        return self.subject_visit.appointment.visit_definition.code

    def requires_poc_vl(self):
        from bhp066.apps.bcpp_subject.classes.rule_group_utilities import func_poc_vl
        return self.panel.name == VIRAL_LOAD and func_poc_vl(self.subject_visit)

    def create_preorder_for_panels(self):
        if self.requires_poc_vl():
            return [POC_VIRAL_LOAD]
        return []

    @property
    def is_poc_vl(self):
        PreOrder = models.get_model('bcpp_lab', 'PreOrder')
        try:
            PreOrder.objects.get(
                subject_visit=self.subject_visit,
                panel__name=POC_VIRAL_LOAD)
            return YES
        except PreOrder.DoesNotExist:
            return NO

    @property
    def optional_description(self):
        """Returns additional text for the packing list item description. See PackingListHelper."""
        try:
            SubjectReferral = models.get_model('bcpp_subject', 'SubjectReferral')
            subject_referral = SubjectReferral.objects.get(subject_visit=self.subject_visit)
            return 'HIV:{} CD4:{} ART:{}'.format(
                subject_referral.hiv_result, subject_referral.cd4_result,
                YES if subject_referral.on_art else NO)
        except SubjectReferral.DoesNotExist:
            return ''
        except AttributeError:
            return ''

    def dispatch_container_lookup(self, using=None):
        return (('bcpp_household', 'Plot'),
                'subject_visit__household_member__household_structure__household__plot__plot_identifier')

    def aliquot(self):
        url = reverse('admin:bcpp_lab_aliquot_changelist')
        return """<a href="{url}?q={requisition_identifier}" />aliquots</a>""".format(
            url=url, requisition_identifier=self.requisition_identifier)
    aliquot.allow_tags = True

    class Meta:
        app_label = 'bcpp_lab'
        verbose_name = 'Subject Requisition'
        unique_together = ('subject_visit', 'panel', 'is_drawn')
        ordering = ('-created', )
