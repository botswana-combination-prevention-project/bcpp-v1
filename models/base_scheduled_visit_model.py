from datetime import datetime
from django.db import models
from bhp_base_model.validators import datetime_not_before_study_start, datetime_not_future
from subject_visit import SubjectVisit
from my_base_uuid_model import MyBaseUuidModel


class BaseScheduledVisitModel(MyBaseUuidModel):

    """ Base model for all scheduled models (adds key to :class:`SubjectVisit`). """

    subject_visit = models.OneToOneField(SubjectVisit)

    report_datetime = models.DateTimeField("Today's date",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),
        )

    def __unicode__(self):
        return unicode(self.subject_visit)

    def get_report_datetime(self):
        return self.subject_visit.report_datetime

    def get_subject_identifier(self):
        return self.subject_visit.get_subject_identifier()

    def get_visit(self):
        return self.subject_visit

    class Meta:
        abstract = True
