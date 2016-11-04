from django.db import models
from django.utils import timezone
from simple_history.models import HistoricalRecords

from edc_base.model.validators.date import datetime_not_future
from edc_base.model.models import BaseUuidModel, UrlMixin
from edc_consent.model_mixins import RequiresConsentMixin
from edc_metadata.model_mixins import UpdatesCrfMetadataModelMixin
from edc_sync.model_mixins import SyncModelMixin
from edc_visit_tracking.managers import CrfModelManager
from edc_visit_tracking.model_mixins import (
    CrfModelMixin as VisitTrackingCrfModelMixin, CrfInlineModelMixin as VisitTrackingCrfInlineModelMixin)

from .subject_visit import SubjectVisit


class CrfModelMixin(SyncModelMixin, VisitTrackingCrfModelMixin, UrlMixin, RequiresConsentMixin,
                    UpdatesCrfMetadataModelMixin, BaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_future, ],
        default=timezone.now,
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    objects = CrfModelManager()

    history = HistoricalRecords()

    def natural_key(self):
        return self.subject_visit.natural_key()

    @property
    def appointment(self):
        return self.visit.appointment

    @property
    def subject_identifier(self):
        return self.get_subject_identifier()

    class Meta(VisitTrackingCrfModelMixin.Meta):
        consent_model = 'bcpp_subject.subjectconsent'
        abstract = True
