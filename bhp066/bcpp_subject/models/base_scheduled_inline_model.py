from datetime import datetime
from django.db import models
from django.core.exceptions import ImproperlyConfigured
from edc.core.bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from edc.core.bhp_consent.models import BaseConsentedUuidModel
from bcpp_household.models import Plot
from .subject_visit import SubjectVisit


class BaseScheduledInlineModel(BaseConsentedUuidModel):

    """ Base model for all scheduled inline models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.ForeignKey(SubjectVisit)

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
        )

    def save(self, *args, **kwargs):
        self.subject_visit = self.inline_parent().subject_visit
        self.report_datetime = self.inline_parent().report_datetime
        super(BaseScheduledInlineModel, self).save(*args, **kwargs)

    def inline_parent(self):
        raise ImproperlyConfigured('Override on the inline model to return the parent model')

    def get_report_datetime(self):
        return self.subject_visit.report_datetime

    def get_subject_identifier(self):
        return self.subject_visit.get_subject_identifier()

    def get_visit(self):
        return self.subject_visit

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'), 'subject_visit__household_member__household_structure__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit__household_member__household_structure__plot__plot_identifier')

    class Meta:
        abstract = True
