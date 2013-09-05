from django.db import models
from bhp_consent.models import BaseConsentHistory
from bcpp_household_member.models import HouseholdMember
from bcpp_survey.models import Survey
from bcpp_subject.managers import ConsentHistoryManager


class SubjectConsentHistory(BaseConsentHistory):

    survey = models.ForeignKey(Survey)

    household_member = models.ForeignKey(HouseholdMember)

    objects = ConsentHistoryManager()

    class Meta:
        app_label = 'bcpp_subject'
