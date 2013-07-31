import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubjectMoved
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectMovedFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectMoved

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    moved_date = date.today()
    moved_reason = (('TRANSFER', u'Job Transfer'), ('MARRIAGE', u'Marriage'), ('INDEPENDENT', u'Independence'), ('OTHER', u'Other'))[0][0]
    moved_reason_other = factory.Sequence(lambda n: 'moved_reason_other{0}'.format(n))
    place_moved = (('IN_VILLAGE', u'Within Village'), ('OUT_VILLAGE', u'Outside Village'), ('IN_WARD', u'Within the Survey Ward'))[0][0]
    area_moved = factory.Sequence(lambda n: 'area_moved{0}'.format(n))
    comment = factory.Sequence(lambda n: 'comment{0}'.format(n))
