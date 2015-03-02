from django.db import models

from edc.subject.consent.models import BaseConsentHistory

from apps.bcpp_household_member.models import HouseholdMember
from apps.bcpp_subject.managers import ConsentHistoryManager
from apps.bcpp_survey.models import Survey


class ClinicConsentHistory(BaseConsentHistory):

    survey = models.ForeignKey(Survey)

    household_member = models.ForeignKey(HouseholdMember)

    objects = ConsentHistoryManager()

    def natural_key(self):
        if not self.registered_subject:
            raise AttributeError("registered_subject cannot be None for pk='\{0}\'".format(self.pk))
        return self.consent_datetime + self.survey + self.registered_subject.natural_key()
    natural_key.dependencies = ['registration.registered_subject']

    class Meta:
        app_label = 'bcpp_clinic'
        verbose_name = 'Clinic Consent History'
        verbose_name_plural = 'Clinic Consent History'

