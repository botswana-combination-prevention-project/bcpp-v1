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
        app_label = 'bhp_registration'                    

"""
    Basic Off study / AF004
"""
class BaseOffStudy(MyBasicUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject)

    offstudy_date = models.DateField(
        verbose_name="Off-study Date",
        help_text="",
        )

    reason = models.CharField(
        verbose_name = "Please code the primary reason participant taken off-study",
        max_length = 25,
        #choices = OFF_STUDY_REASON,
        )

    reason_other = OtherCharField()

    comment = models.CharField(
        max_length=35,
        verbose_name="Comments:",
        blank=True,
        null=True,   
        ) 
        
    class Meta:
        app_label = 'bhp_registration'
        abstract = True
        

