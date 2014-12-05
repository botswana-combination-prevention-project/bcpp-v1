import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_survey.tests.factories import SurveyFactory
from ...models import CallLog


class CallLogFactory(BaseUuidModelFactory):
    FACTORY_FOR = CallLog

    household_member = factory.SubFactory(HouseholdMemberFactory)
    survey = factory.SubFactory(SurveyFactory)
    label = factory.Sequence(lambda n: 'label{0}'.format(n))
    locator_information = factory.Sequence(lambda n: 'locator_information{0}'.format(n))
