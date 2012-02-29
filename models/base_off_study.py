from django.db import models
from bhp_common.fields import OtherCharField
from base_registered_subject_model import BaseRegisteredSubjectModel

"""
    Basic Off study / AF004
"""
class BaseOffStudy(BaseRegisteredSubjectModel):

    #registered_subject = models.OneToOneField(RegisteredSubject)

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

    comment = models.TextField(
        max_length=250,
        verbose_name="Comments:",
        blank=True,
        null=True,   
        ) 
      
    class Meta:
        app_label = 'bhp_registration'
        abstract = True
        

