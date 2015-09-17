from django.db import models

from edc_base.audit_trail import AuditTrail
from edc.subject.visit_tracking.models import BaseVisitTracking

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.choices import VISIT_UNSCHEDULED_REASON


class HtcSubjectVisit(BaseVisitTracking):

    household_member = models.ForeignKey(HouseholdMember)

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON,
        )

    history = AuditTrail()

    def save(self, *args, **kwargs):
        self.info_source = 'subject'
        self.reason = 'consent'
        super(HtcSubjectVisit, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.appointment)

    def dispatch_container_lookup(self):
        return (('bcpp_household', 'Household'), 'household_member__household_structure__household__household_identifier')

    class Meta:
        app_label = "bcpp_htc_subject"
        verbose_name = "HTC Subject Visit"
