from django.db import models
from django.utils.translation import ugettext_lazy as _

from edc.audit.audit_trail import AuditTrail
from edc.base.model.fields import OtherCharField
from edc.base.model.validators import date_not_future, date_not_before_study_start
from edc.choices.common import GENDER
from edc.core.bhp_variables.models import StudySite

from .base_clinic_registered_subject_model import BaseClinicRegisteredSubjectModel


class ClinicRefusal (BaseClinicRegisteredSubjectModel):

    refusal_date = models.DateField(
        verbose_name=_("Date subject refused participation"),
        validators=[date_not_before_study_start, date_not_future],
        help_text="Date format is YYYY-MM-DD")

    site = models.ForeignKey(StudySite, null=True)

    reason = models.CharField(
        verbose_name=_("We respect your decision to decline. It would help us"
                       " improve the study if you could tell us the main reason"
                       " you do not want to participate in this study?"),
        max_length=50,
        choices=(('dont_want', 'I don\'t want to take part'),
                 ('not_sure', 'I am not sure'),
                 ('dont_want_blood_draw', 'I don\'t want to have blood drawn'),
                 ('needles_phobia', 'Fear of needles'),
                 ('privacy', 'I am afraid my information will not be private'),
                 ('illiterate no witness', 'Illiterate does not want a witness'),
                 ('on_haart', 'Already on HAART'),
                 ('knows_status', 'I already know my status'),
                 ('OTHER', 'Other, specify')),
        help_text="")

    reason_other = OtherCharField()

    gender = models.CharField(
        verbose_name='Gender',
        max_length=1,
        choices=GENDER)

    comment = models.CharField(
        verbose_name=_("Comment"),
        max_length=250,
        null=True,
        blank=True,
        help_text=_('IMPORTANT: Do not include any names or other personally identifying '
                    'information in this comment'))

    history = AuditTrail()

    def get_registration_datetime(self):
        return self.report_datetime

    def __unicode__(self):
        return "for participant"

    class Meta:
        app_label = "bcpp_clinic"
        verbose_name = "Subject Refusal"
        verbose_name_plural = "Subject Refusal"
