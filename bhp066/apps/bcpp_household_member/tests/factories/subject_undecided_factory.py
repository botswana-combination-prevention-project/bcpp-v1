import factory

from datetime import datetime

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import SubjectUndecided

from .household_member_factory import HouseholdMemberFactory


class SubjectUndecidedFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectUndecided

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
