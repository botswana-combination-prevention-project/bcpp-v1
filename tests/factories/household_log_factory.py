import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import HouseholdLog
from bcpp_household.tests.factories import HouseholdFactory
from bcpp_survey.tests.factories import SurveyFactory


class HouseholdLogFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdLog

    household = factory.SubFactory(HouseholdFactory)
    survey = factory.SubFactory(SurveyFactory)
