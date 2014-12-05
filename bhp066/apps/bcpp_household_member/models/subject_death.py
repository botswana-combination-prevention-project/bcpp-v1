from django.db import models
from datetime import datetime, time

from edc.audit.audit_trail import AuditTrail
from edc.base.model.validators import date_not_before_study_start, date_not_future
#from edc.subject.adverse_event.models import BaseBaseDeath
from edc.subject.registration.models import BaseRegisteredSubjectModel


class SubjectDeath(BaseRegisteredSubjectModel):

    date_death_reported = models.DateField(
        verbose_name="Date Death Reported:",
        validators=[
            date_not_before_study_start,
            date_not_future,
            ],
        help_text="",
        )

    history = AuditTrail()

    def __unicode__(self):
        return unicode(self.registered_subject)

    def get_report_datetime(self):
        return datetime.combine(self.death_date, time(0, 0))

    class Meta:
        app_label = "bcpp_household_member"
        verbose_name = "Subject Death"
        verbose_name_plural = "Subject Death"
