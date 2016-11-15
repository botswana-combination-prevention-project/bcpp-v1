from django.db import models

from edc_base.model.models import BaseUuidModel, HistoricalRecords
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import CreatesMetadataModelMixin
from edc_visit_tracking.managers import VisitModelManager
from edc_visit_tracking.model_mixins import VisitModelMixin

from bcpp_household_member.models import HouseholdMember

from ..choices import VISIT_UNSCHEDULED_REASON

from .appointment import Appointment


class SubjectVisit(VisitModelMixin, CreatesMetadataModelMixin, RequiresConsentMixin, BaseUuidModel):

    """A model completed by the user that captures the covering information for the data collected
    for this timepoint/appointment, e.g.report_datetime."""

    appointment = models.OneToOneField(Appointment)

    household_member = models.ForeignKey(HouseholdMember)

    reason_unscheduled = models.CharField(
        verbose_name="If 'Unscheduled' above, provide reason for the unscheduled visit",
        max_length=25,
        blank=True,
        null=True,
        choices=VISIT_UNSCHEDULED_REASON,
    )

    objects = VisitModelManager()

    history = HistoricalRecords()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.household_member.registered_subject.subject_identifier
        self.info_source = 'subject'
        self.reason = 'consent'
        super(SubjectVisit, self).save(*args, **kwargs)

    class Meta:
        app_label = "bcpp_subject"
        verbose_name = "Subject Visit"
        consent_model = 'bcpp_subject.subjectconsent'
