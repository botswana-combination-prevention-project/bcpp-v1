from django.db import models
from bhp_base_model.fields import OtherCharField
from bhp_registration.models import BaseRegisteredSubjectModel
from bhp_crypto.utils import mask_encrypted

class BaseOffStudy(BaseRegisteredSubjectModel):

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

    def __unicode__(self):
        return "{0} {1} ({2})".format(self.registered_subject.subject_identifier,
                                          self.registered_subject.subject_type,
                                          mask_encrypted(self.registered_subject.first_name))

    class Meta:
        app_label = 'bhp_off_study'
        abstract = True

