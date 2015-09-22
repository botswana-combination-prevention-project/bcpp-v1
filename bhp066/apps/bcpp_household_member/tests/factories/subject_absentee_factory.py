import factory

from datetime import datetime

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import SubjectAbsentee

from .household_member_factory import HouseholdMemberFactory


class SubjectAbsenteeFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectAbsentee

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
