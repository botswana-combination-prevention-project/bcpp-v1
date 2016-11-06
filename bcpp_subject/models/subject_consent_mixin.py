from django.db import models

from edc_constants.choices import YES_NO

from bcpp.models import RegisteredSubject
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey

from ..choices import COMMUNITIES


class SubjectConsentMixin(models.Model):

    household_member = models.ForeignKey(HouseholdMember, help_text='')

    study_site = models.CharField(
        verbose_name='Site',
        max_length=15,
        null=True,
        help_text="This refers to the site or 'clinic area' where the subject is being consented.",
        editable=False,
    )

    is_minor = models.CharField(
        verbose_name=("Is subject a minor?"),
        max_length=10,
        null=True,
        blank=False,
        default='-',
        choices=YES_NO,
        help_text=('Subject is a minor if aged 16-17. A guardian must be present for consent. '
                   'HIV status may NOT be revealed in the household.'),
        editable=False,
    )

    is_signed = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return '{0} ({1}) V{2}'.format(self.subject_identifier, self.survey, self.version)

    class Meta:
        abstract = True
