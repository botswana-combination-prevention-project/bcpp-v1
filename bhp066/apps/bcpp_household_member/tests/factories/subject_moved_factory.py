import factory

from datetime import date, datetime

from edc.subject.registration.tests.factories import RegisteredSubjectFactory

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import SubjectMoved

from .household_member_factory import HouseholdMemberFactory


class SubjectMovedFactory(factory.DjangoModelFactory):

    class Meta:
        model = SubjectMoved

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    moved_date = date.today()
    moved_reason = (('TRANSFER', u'Job Transfer'), ('MARRIAGE', u'Marriage'), ('INDEPENDENT', u'Independence'), ('OTHER', u'Other'))[0][0]
    moved_reason_other = factory.Sequence(lambda n: 'moved_reason_other{0}'.format(n))
    place_moved = (('IN_VILLAGE', u'Within Village'), ('OUT_VILLAGE', u'Outside Village'))[0][0]
    area_moved = factory.Sequence(lambda n: 'area_moved{0}'.format(n))
    comment = factory.Sequence(lambda n: 'comment{0}'.format(n))
