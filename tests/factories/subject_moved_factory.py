import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SubjectMoved
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectMovedFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SubjectMoved

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    moved_date = date.today()
    moved_reason = (('TRANSFER', 'Job Transfer'), ('MARRIAGE', 'Marriage'), ('INDEPENDENT', 'Independence'), ('OTHER', 'Other'))[0][0]
    moved_reason_other = factory.Sequence(lambda n: 'moved_reason_other{0}'.format(n))
    place_moved = (('IN_VILLAGE', 'Within Village'), ('OUT_VILLAGE', 'Outside Village'), ('IN_WARD', 'Within the Survey Ward'))[0][0]
    area_moved = factory.Sequence(lambda n: 'area_moved{0}'.format(n))
    comment = factory.Sequence(lambda n: 'comment{0}'.format(n))
