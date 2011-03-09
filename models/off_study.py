from django.db import models
from bhp_common.models import MyBasicListModel, MyBasicUuidModel
from bhp_common.fields import OtherCharField
from bhp_common.validators import datetime_not_before_study_start, datetime_not_future
from bhp_registration.choices import SUBJECT_TYPE
from registered_subject import RegisteredSubject

class OffStudyReason (MyBasicListModel):

    subject_type = models.CharField(
        max_length = 25,
        choices=SUBJECT_TYPE,
        )         

    class Meta:
        ordering = ['display_index'] 

"""
    Basic Off study / AF004
"""
class OffStudy(MyBasicUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject)

    off_study_date=models.DateField(
        verbose_name="Off-study Date",
        help_text="",
        )

    reason_off_study = models.ForeignKey(OffStudyReason,
        verbose_name="Please code the primary reason for why the subject is being taken off-study",
        help_text="",
        )

    reason_off_study_other = OtherCharField()

    comment = models.CharField(
        max_length=35,
        verbose_name="Comments:",
        blank=True,
        null=True,   
        ) 

