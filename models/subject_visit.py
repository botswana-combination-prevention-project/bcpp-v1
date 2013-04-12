from django.db import models
from django.core.urlresolvers import reverse
from audit_trail.audit import AuditTrail
from bhp_visit_tracking.models import BaseVisitTracking
from bcpp_subject.choices import VISIT_UNSCHEDULED_REASON


class SubjectVisit(BaseVisitTracking):

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON,
        )

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.appointment)

    def get_absolute_url(self):
        return reverse('admin:bcpp_subject_subjectvisit_change', args=(self.id,))

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Visit"
