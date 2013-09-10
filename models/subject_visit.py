from django.db import models
from audit_trail.audit import AuditTrail
from bhp_visit_tracking.models import BaseVisitTracking
from bcpp_subject.choices import VISIT_UNSCHEDULED_REASON
from subject_off_study_mixin import SubjectOffStudyMixin
from bcpp_household_member.models import HouseholdMember


class SubjectVisit(SubjectOffStudyMixin, BaseVisitTracking):

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
        return (('bcpp_household', 'Household'), 'household_member__household_structure__household__household_identifier')

#     def post_save_update_appt_status(self):
#         """Sets the appointment appt_status to 'in progress' as a convenience to the user editing a subject visit."""
#         dirty = False
#         if 'C' in self.appointment.visit_definition.code and not self.appointment.appt_status == 'done':
#             self.appointment.appt_status = 'in_progress'
#             dirty = True
#         if self.reason == 'refuse' or self.reason == 'absent' or self.reason == 'undecided':
#             self.appointment.appt_status = 'done'
#             dirty = True
#         if dirty:
#             self.appointment.save()

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Visit"
