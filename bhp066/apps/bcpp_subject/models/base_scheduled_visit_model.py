from datetime import datetime

from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.consent.models import BaseConsentedUuidModel

from apps.bcpp_household.models import Plot

from ..managers import ScheduledModelManager

from .subject_off_study_mixin import SubjectOffStudyMixin
from .subject_visit import SubjectVisit
# from ..constants import RBD, FULL, Questionnaires, HTC


class BaseScheduledVisitModel(SubjectOffStudyMixin, BaseConsentedUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField(
        verbose_name="Report Date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
#         auto_now=False,
        default=datetime.now,  # By passing datetime.now without the parentheses, you are passing the actual function, which will be called each time a record is added ref: http://stackoverflow.com/questions/2771676/django-default-datetime-now-problem
        help_text=('If reporting today, use today\'s date/time, otherwise use '
                   'the date/time this information was reported.'))

    objects = ScheduledModelManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(SubjectVisit)

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

    @classmethod
    def visit_model(self):
        """Used by search in audit_trail"""
        return SubjectVisit

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'), 'subject_visit__household_member__household_structure__household__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'subject_visit__household_member__household_structure__household__plot__plot_identifier')

    def deserialize_get_missing_fk(self, attrname):
        retval = None
        if attrname == 'subject_visit':
            return self.subject_visit
        return retval

    def bypass_meta_data(self):
        return False

    class Meta:
        abstract = True
