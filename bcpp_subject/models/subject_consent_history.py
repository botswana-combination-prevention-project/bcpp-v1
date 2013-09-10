from django.db import models
from bhp_consent.models import BaseConsentHistory
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey
from bcpp_subject.managers import ConsentHistoryManager


class SubjectConsentHistory(BaseConsentHistory):

    survey = models.ForeignKey(Survey)

    household_member = models.ForeignKey(HouseholdMember)

    objects = ConsentHistoryManager()
    
    def natural_key(self):
        if not self.registered_subject:
            raise AttributeError("registered_subject cannot be None for pk='\{0}\'".format(self.pk))
        return self.consent_datetime + self.survey + self.registered_subject.natural_key()
    natural_key.dependencies = ['bhp_registration.registered_subject']

    class Meta:
        app_label = 'bcpp_subject'
