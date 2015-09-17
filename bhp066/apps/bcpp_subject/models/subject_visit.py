from django.db import models

from edc.device.dispatch.models import BaseDispatchSyncUuidModel
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc_base.audit_trail import AuditTrail
from edc.device.sync.models import BaseSyncUuidModel
from edc_consent.models import RequiresConsentMixin

from bhp066.apps.bcpp_household_member.models import HouseholdMember

from ..choices import VISIT_UNSCHEDULED_REASON

from .subject_off_study_mixin import SubjectOffStudyMixin


class SubjectVisit(SubjectOffStudyMixin, RequiresConsentMixin, BaseVisitTracking,
                   BaseDispatchSyncUuidModel, BaseSyncUuidModel):

    CONSENT_MODEL = models.get_model('bcpp_subject', 'SubjectConsent')

    household_member = models.ForeignKey(HouseholdMember)

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON,
    )

    history = AuditTrail(True)

    def save(self, *args, **kwargs):
        self.info_source = 'subject'
        self.reason = 'consent'
        super(SubjectVisit, self).save(*args, **kwargs)

    def __unicode__(self):
        return '{} {} ({}) {}'.format(self.appointment.registered_subject.subject_identifier,
                                      self.appointment.registered_subject.first_name,
                                      self.appointment.registered_subject.gender,
                                      self.appointment.visit_definition.code)

    def dispatch_container_lookup(self):
        return (('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Visit"
