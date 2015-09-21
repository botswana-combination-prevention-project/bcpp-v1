import factory
from datetime import datetime

from edc.testing.tests.factories.test_consent_factory import BaseConsentFactory
from edc.core.bhp_variables.tests.factories import StudySiteFactory

from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory

from bhp066.apps.bcpp_survey.tests.factories import SurveyFactory

from ...models import HtcSubjectConsent


class HtcSubjectConsentFactory(BaseConsentFactory):
    FACTORY_FOR = HtcSubjectConsent

    subject_identifier = factory.Sequence(lambda n: 'subject_identifier{0}'.format(n))
    study_site = factory.SubFactory(StudySiteFactory)
    consent_datetime = datetime.today()
    may_store_samples = 'No'
    is_incarcerated = 'No'
    is_literate = 'Yes'
    consent_version_on_entry = 2
    consent_version_recent = 2
    language = (('tn', 'Setswana'), ('en', 'English'))[0][0]
    is_verified = True
    identity = factory.Sequence(lambda n: 'identity{0}'.format(n))
    identity_type = (('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other'))[0][0]
    household_member = factory.SubFactory(HouseholdMemberFactory)
    survey = factory.SubFactory(SurveyFactory)
    is_signed = True
