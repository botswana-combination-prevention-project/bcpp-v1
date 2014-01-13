from django.db import models
from edc.audit.audit_trail import AuditTrail
from edc.subject.visit_tracking.models import BaseVisitTracking
from apps.bcpp_subject.choices import VISIT_UNSCHEDULED_REASON
from .clinic_off_study_mixin import ClinicOffStudyMixin


class ClinicVisit(ClinicOffStudyMixin, BaseVisitTracking):

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

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Clinic Visit"
        verbose_name_plural = "Clinic Visit"
