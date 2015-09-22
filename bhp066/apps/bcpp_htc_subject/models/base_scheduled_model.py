from datetime import datetime
from django.db import models
from edc_base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.subject.consent.models import BaseConsentedUuidModel
from bhp066.apps.bcpp_household.models import Plot
from ..managers import ScheduledModelManager
from .htc_subject_visit import HtcSubjectVisit


class BaseScheduledModel(BaseConsentedUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    htc_subject_visit = models.OneToOneField(HtcSubjectVisit)

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
        )

    objects = ScheduledModelManager()

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.get_visit())

    def get_report_datetime(self):
        return self.get_visit().report_datetime

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_visit(self):
        return self.htc_subject_visit

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'), 'htc_subject_visit__household_member__household_structure__household__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'htc_subject_visit__household_member__household_structure__household__plot__plot_identifier')

    class Meta:
        abstract = True
