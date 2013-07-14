import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import SubjectRefusal
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectRefusalFactory(BaseScheduledModelFactory):
    FACTORY_FOR = SubjectRefusal

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    sex = (('M', 'Male'), ('F', 'Female'))[0][0]
    age = factory.Sequence(lambda n: 'age{0}'.format(n))
    length_residence = (('Less than 6 months', 'Less than 6 months'), ('6 months to 12 months', '6 months to 12 months'), ('1 to 5 years', '1 to 5 years'), ('More than 5 years', 'More than 5 years'), ("Don't want to answer", "Don't want to answer"))[0][0]
    refusal_date = date.today()
    why_no_participate = (("I don't have time", "I don't have time"), ("I don't want to answer the questions", "I don't want to answer the questions"), ("I don't want to have the blood drawn", "I don't want to have the blood drawn"), ('I am afraid my information will not be private', 'I am afraid my information will not be private'), ('I am not sure', 'I am not sure'), ('Other, specify:', 'Other, specify:'), ("Don't want to answer", "Don't want to answer"))[0][0]
    why_no_participate_other = factory.Sequence(lambda n: 'why_no_participate_other{0}'.format(n))
    subject_refusal_status = factory.Sequence(lambda n: 'subject_refusal_status{0}'.format(n))
    hiv_test_today = (('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure'))[0][0]
