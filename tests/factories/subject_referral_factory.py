import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import SubjectReferral
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bcpp_survey.tests.factories import SurveyFactory


class SubjectReferralFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectReferral

    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    survey = factory.SubFactory(SurveyFactory)
    subject_referral_reason = (('receive', u'Referred to receive HIV result in clinic'), ('test', u'Referred to test in clinic'), ('protocol', u'Referred as per protocol'))[0][0]
    subject_referral_reason_other = factory.Sequence(lambda n: 'subject_referral_reason_other{0}'.format(n))
    in_clinic = (('Yes', '<django.utils.functional.__proxy__ object at 0x1021b8810>'), ('No', '<django.utils.functional.__proxy__ object at 0x1021b8850>'))[0][0]
    comment = factory.Sequence(lambda n: 'comment{0}'.format(n))
