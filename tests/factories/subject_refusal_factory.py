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
    sex = (('M', 'Male'), ('F', 'Female'))[0][0]
    age = factory.Sequence(lambda n: 'age{0}'.format(n))
    length_residence = (('Less than 6 months', <django.utils.functional.__proxy__ object at 0x103ae4490>), ('6 months to 12 months', <django.utils.functional.__proxy__ object at 0x103ae4510>), ('1 to 5 years', <django.utils.functional.__proxy__ object at 0x103ae4590>), ('More than 5 years', <django.utils.functional.__proxy__ object at 0x103ae4610>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103ae4690>))[0][0]
    refusal_date = date.today()
    why_no_participate = (("I don't have time", <django.utils.functional.__proxy__ object at 0x103d03950>), ("I don't want to answer the questions", <django.utils.functional.__proxy__ object at 0x103d039d0>), ("I don't want to have the blood drawn", <django.utils.functional.__proxy__ object at 0x103d03a50>), ('I am afraid my information will not be private', <django.utils.functional.__proxy__ object at 0x103d03ad0>), ('I am not sure', <django.utils.functional.__proxy__ object at 0x103d03b50>), ('Other, specify:', <django.utils.functional.__proxy__ object at 0x103d03bd0>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103d03c50>))[0][0]
    why_no_participate_other = factory.Sequence(lambda n: 'why_no_participate_other{0}'.format(n))
    subject_refusal_status = factory.Sequence(lambda n: 'subject_refusal_status{0}'.format(n))
    hiv_test_today = (('Yes', 'Yes'), ('No', 'No'), ('Not Sure', 'Not Sure'))[0][0]
