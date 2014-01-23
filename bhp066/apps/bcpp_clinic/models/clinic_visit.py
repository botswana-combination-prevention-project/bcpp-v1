from django.db import models

from edc.audit.audit_trail import AuditTrail
# from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_tracking.models import BaseVisitTracking

from ..choices import VISIT_UNSCHEDULED_REASON

from .clinic_off_study_mixin import ClinicOffStudyMixin


class ClinicVisit(ClinicOffStudyMixin, BaseVisitTracking):

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON,
        )

#     registered_subject = models.ForeignKey(RegisteredSubject, null=True, editable=False)

    history = AuditTrail()

    @property
    def registered_subject(self):
        return self.get_registered_subject()

    def __unicode__(self):
        return unicode(self.appointment)

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Visit"
        verbose_name_plural = "Clinic Visit"
