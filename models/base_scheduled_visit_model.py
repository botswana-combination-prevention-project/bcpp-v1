from datetime import datetime
from django.db import models
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from bhp_consent.models import BaseConsentedUuidModel
from bcpp_household.models import Household
from bcpp_subject.managers import ScheduledModelManager
from subject_visit import SubjectVisit
from subject_off_study_mixin import SubjectOffStudyMixin


class BaseScheduledVisitModel(SubjectOffStudyMixin, BaseConsentedUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
        )

    objects = ScheduledModelManager()

    def natural_key(self):
        return self.subject_visit.natural_key()
    
    def __unicode__(self):
        return unicode(self.subject_visit)

    def get_report_datetime(self):
        return self.subject_visit.report_datetime

    def get_subject_identifier(self):
        return self.subject_visit.get_subject_identifier()

    def get_visit(self):
        return self.subject_visit

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'household'), 'subject_visit__household_member__household_structure__household')

    def dispatch_container_lookup(self, using=None):
        return (Household, 'subject_visit__household_member__household_structure__household__household_identifier')

    class Meta:
        abstract = True
