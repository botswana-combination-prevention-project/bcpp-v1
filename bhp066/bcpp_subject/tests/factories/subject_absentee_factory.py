import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubjectAbsentee
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectAbsenteeFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectAbsentee

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    subject_absentee_status = (('ABSENT', u'Absent'), ('NOT_ABSENT', u'No longer absent'))[0][0]
