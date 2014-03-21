import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import SubjectRefusal
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
# from apps.bcpp_survey.tests.factories import SurveyFactory


class SubjectRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectRefusal

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
#     survey = factory.SubFactory(SurveyFactory)
    refusal_date = date.today()
    reason = (("I don't have time", u"I don't have time"), ("I don't want to answer the questions", u"I don't want to answer the questions"), ("I don't want to have the blood drawn", u"I don't want to have the blood drawn"), ('I am afraid my information will not be private', u'I am afraid my information will not be private'), ('not_sure', u'I am not sure'), ('OTHER', u'Other, specify:'), ('not_answering', u"Don't want to answer"))[0][0]
    reason_other = factory.Sequence(lambda n: 'reason_other{0}'.format(n))
    subject_refusal_status = factory.Sequence(lambda n: 'subject_refusal_status{0}'.format(n))
