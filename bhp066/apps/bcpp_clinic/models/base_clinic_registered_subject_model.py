from datetime import datetime
from django.db import models
from edc.subject.registration.models import BaseRegisteredSubjectModel
from edc.base.model.validators import datetime_not_before_study_start, datetime_not_future
from clinic_off_study_mixin import ClinicOffStudyMixin


class BaseClinicRegisteredSubjectModel(ClinicOffStudyMixin, BaseRegisteredSubjectModel):

    registration_datetime = models.DateTimeField("Today's date/time",
        validators=[
            datetime_not_before_study_start,
            datetime_not_future, ],
        default=datetime.today(),)

    def get_report_datetime(self):
        return self.registration_datetime

    class Meta:
        abstract = True
