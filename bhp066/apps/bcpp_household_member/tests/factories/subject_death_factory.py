import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.adverse_event.tests.factories import (DeathCauseCategoryFactory, DeathCauseInfoFactory, 
                                                       DeathMedicalResponsibilityFactory)
from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import SubjectDeath

from .household_member_factory import HouseholdMemberFactory


class SubjectDeathFactory(BaseUuidModelFactory):

    class Meta:
        model = SubjectDeath

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    site_aware_date = datetime.today()
    duration_of_illness = 10
    survey = factory.SubFactory(SurveyFactory)
    death_date = datetime(2015, 4, 11)
    site_aware_date = datetime.today()
    primary_medical_care_giver = factory.SubFactory(DeathMedicalResponsibilityFactory)
#     participant_hospitalized = 'No'
    death_cause_category = factory.SubFactory(DeathCauseCategoryFactory)
    death_cause_info = factory.SubFactory(DeathCauseInfoFactory)
