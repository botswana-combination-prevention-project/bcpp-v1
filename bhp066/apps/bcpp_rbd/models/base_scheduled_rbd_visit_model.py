from datetime import datetime

from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.subject.consent.models import BaseConsentedUuidModel

from apps.bcpp_household.models import Plot
from apps.bcpp_subject.models import SubjectOffStudyMixin

from ..managers import ScheduledRBDModelManager

from .rbd_visit import RBDVisit


class BaseScheduledRBDVisitModel(SubjectOffStudyMixin, BaseConsentedUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    rbd_visit = models.OneToOneField(RBDVisit)

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
        )

    objects = ScheduledRBDModelManager()

    history = AuditTrail()

    entry_meta_data_manager = EntryMetaDataManager(RBDVisit)

    def natural_key(self):
        return self.get_visit().natural_key()

    def __unicode__(self):
        return unicode(self.get_visit())

    def get_report_datetime(self):
        return self.get_visit().report_datetime

    def get_subject_identifier(self):
        return self.get_visit().get_subject_identifier()

    def get_visit(self):
        return self.rbd_visit

    def is_dispatched_item_within_container(self, using=None):
        return (('bcpp_household', 'plot'), 'rbd_visit__household_member__household_structure__household__plot')

    def dispatch_container_lookup(self, using=None):
        return (Plot, 'rbd_visit__household_member__household_structure__household__plot__plot_identifier')

    def deserialize_get_missing_fk(self, attrname):  # FIX ME, return subject visit
        retval = None
        if attrname == 'rbd_visit':
            return self.rbd_visit
        return retval

    class Meta:
        abstract = True
