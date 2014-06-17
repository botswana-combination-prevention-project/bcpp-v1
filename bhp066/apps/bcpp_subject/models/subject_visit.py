from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.subject.visit_tracking.models import BaseVisitTracking

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_list.models import Religion

from ..choices import VISIT_UNSCHEDULED_REASON

from .subject_off_study_mixin import SubjectOffStudyMixin


class SubjectVisit(SubjectOffStudyMixin, BaseVisitTracking):
    
    #religion= models.ForeignKey(Religion)

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
        super(SubjectVisit, self).save(*args, **kwargs)

    def __unicode__(self):
        return unicode(self.appointment)

    def dispatch_container_lookup(self):
        return (('bcpp_household', 'Plot'), 'household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Visit"
