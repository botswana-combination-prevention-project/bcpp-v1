from django.db import models

from edc_base.audit_trail import AuditTrail
from edc_base.model.fields import OtherCharField

from bhp066.apps.bcpp.choices import YES_NO_UNSURE, YES_NO, COMMUNITY_NA

from .base_scheduled_visit_model import BaseScheduledVisitModel
from .subject_consent import SubjectConsent


class Circumcision (BaseScheduledVisitModel):

    CONSENT_MODEL = SubjectConsent

    circumcised = models.CharField(
        verbose_name="Are you circumcised?",
        max_length=15,
        choices=YES_NO_UNSURE,
        help_text="")

    last_seen_circumcised = models.CharField(
        verbose_name="Since we last spoke with you on last_seen_circumcised, have you been circumcised?",
        max_length=15,
        null=True,
        blank=True,
        choices=YES_NO,
        help_text="")

    circumcised_datetime = models.DateField(
        verbose_name='If Yes, date?',
        default=None,
        null=True,
        blank=True,
        help_text=""
    )

    circumcised_location = models.CharField(
        verbose_name="IF YES, Location?",
        max_length=25,
        choices=COMMUNITY_NA,
        null=True,
        blank=True,
        help_text="")

    circumcised_location_other = OtherCharField()

    history = AuditTrail()

    def previous_appt(self):
        from edc.subject.appointment.models import Appointment
        registered_subject = self.subject_visit.appointment.registered_subject
        timepoints = range(0, self.subject_visit.appointment.visit_definition.time_point)
        if len(timepoints) > 0:
            timepoints.reverse()
        for point in timepoints:
            try:
                return Appointment.objects.get(registered_subject=registered_subject,
                                               visit_definition__time_point=point)
            except Appointment.DoesNotExist:
                pass
        return None

    class Meta:
        app_label = 'bcpp_subject'
        verbose_name = "Circumcision"
        verbose_name_plural = "Circumcision"
