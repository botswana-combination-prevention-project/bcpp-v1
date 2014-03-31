import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import SubjectUndecided


class SubjectUndecidedFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectUndecided

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
