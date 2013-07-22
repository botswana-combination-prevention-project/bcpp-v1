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
    moved_reason = (('TRANSFER', <django.utils.functional.__proxy__ object at 0x103a23d50>), ('MARRIAGE', <django.utils.functional.__proxy__ object at 0x103a23dd0>), ('INDEPENDENT', <django.utils.functional.__proxy__ object at 0x103a23e50>), ('OTHER', <django.utils.functional.__proxy__ object at 0x103a23ed0>))[0][0]
    moved_reason_other = factory.Sequence(lambda n: 'moved_reason_other{0}'.format(n))
    place_moved = (('IN_VILLAGE', <django.utils.functional.__proxy__ object at 0x103a23f50>), ('OUT_VILLAGE', <django.utils.functional.__proxy__ object at 0x103a23fd0>), ('IN_WARD', <django.utils.functional.__proxy__ object at 0x103a25090>))[0][0]
    area_moved = factory.Sequence(lambda n: 'area_moved{0}'.format(n))
    comment = factory.Sequence(lambda n: 'comment{0}'.format(n))
