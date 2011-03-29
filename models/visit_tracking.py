from django.db import models
from django.core.validators import MinLengthValidator, MaxLengthValidator, RegexValidator
from django.core.validators import RegexValidator, MinValueValidator, MaxValueValidator
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future, datetime_is_future, datetime_is_after_consent
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_registration.models import RegisteredSubject
from bhp_registration.choices import SUBJECT_TYPE
from bhp_visit.models import RegisteredSubjectAppointment





        

