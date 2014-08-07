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
from ..constants import RBD, FULL, Questionnaires, HTC


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

    @property
    def participation_type_string(self):
        from django.db.models import get_model
        participation = get_model('bcpp_subject', 'participation')
        instance = participation.objects.filter(subject_visit=self.subject_visit)
        if instance.exists() and instance[0].participation_type == 'RBD Only':
            return RBD
        if instance.exists() and instance[0].participation_type == 'Questionnaires':
            return Questionnaires
        if instance.exists() and instance[0].participation_type == 'HTC Only':
            return HTC
        #Always default to BHS full participation unless participation model is filled and indicates otherwise.
        return FULL

    class Meta:
        abstract = True
