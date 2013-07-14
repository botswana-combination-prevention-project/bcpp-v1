import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SubjectAbsentee
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectAbsenteeFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SubjectAbsentee

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    subject_absentee_status = (('ABSENT', 'Absent'), ('NOT_ABSENT', 'No longer absent'))[0][0]
