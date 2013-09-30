from datetime import datetime
from django.db import models
from edc.core.bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from edc.core.bhp_consent.models import BaseConsentedUuidModel
from edc.core.audit_trail.audit import AuditTrail
from bcpp_household.models import Plot
from ..managers import ScheduledModelManager
from .subject_visit import SubjectVisit
from .subject_off_study_mixin import SubjectOffStudyMixin


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

    history = AuditTrail()

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.get_visit())

    def get_report_datetime(self):
        return self.get_visit().report_datetime

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_visit(self):
        return self.subject_visit

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'), 'subject_visit__household_member__household_structure__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit__household_member__household_structure__plot__plot_identifier')

    class Meta:
        abstract = True
