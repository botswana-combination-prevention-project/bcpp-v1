import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.adverse_event.tests.factories import DeathCauseCategoryFactory, DeathCauseInfoFactory, DeathMedicalResponsibilityFactory
from apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import SubjectDeath

from .household_member_factory import HouseholdMemberFactory


class SubjectDeathFactory(BaseUuidModelFactory):

    class Meta:
        model = SubjectDeath

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    death_date = datetime(2015, 4, 11)
    participant_hospitalized = 'No'
    primary_medical_care_giver = factory.SubFactory(DeathMedicalResponsibilityFactory)
    relationship_death_study = 'Definitely not related'
    site_aware_date = datetime.today()
#     participant_hospitalized = 'No'
    death_cause_category = factory.SubFactory(DeathCauseCategoryFactory)
    death_cause_info = factory.SubFactory(DeathCauseInfoFactory)
