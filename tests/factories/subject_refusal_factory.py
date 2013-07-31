import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubjectRefusal
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectRefusal

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    sex = (('M', <django.utils.functional.__proxy__ object at 0x101d48910>), ('F', <django.utils.functional.__proxy__ object at 0x101d489d0>))[0][0]
    age = factory.Sequence(lambda n: 'age{0}'.format(n))
    length_residence = (('Less than 6 months', u'Less than 6 months'), ('6 months to 12 months', u'6 months to 12 months'), ('1 to 5 years', u'1 to 5 years'), ('More than 5 years', u'More than 5 years'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    refusal_date = date.today()
    why_no_participate = (("I don't have time", u"I don't have time"), ("I don't want to answer the questions", u"I don't want to answer the questions"), ("I don't want to have the blood drawn", u"I don't want to have the blood drawn"), ('I am afraid my information will not be private', u'I am afraid my information will not be private'), ('I am not sure', u'I am not sure'), ('Other, specify:', u'Other, specify:'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    why_no_participate_other = factory.Sequence(lambda n: 'why_no_participate_other{0}'.format(n))
    subject_refusal_status = factory.Sequence(lambda n: 'subject_refusal_status{0}'.format(n))
    hiv_test_today = (('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure'))[0][0]
