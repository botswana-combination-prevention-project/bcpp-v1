import factory
from datetime import datetime, date
from edc.testing.tests.factories.test_consent_factory import BaseConsentFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import SubjectConsent
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory


class SubjectConsentFactory(BaseConsentFactory):

    class Meta:
        model = SubjectConsent

    household_member = factory.SubFactory(HouseholdMemberFactory)
    subject_identifier = None
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    consent_datetime = datetime.today()
    may_store_samples = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    is_literate = (('Yes', 'Yes'), ('No', 'No'))[0][0]
    consent_version_on_entry = 1
    consent_version_recent = 1
    gender = 'M'
    dob = date(1980, 01, 01)
    citizen = 'Yes'
    is_verified = True
    identity = factory.Sequence(lambda n: 'identity{0}'.format(n))
    identity_type = (('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other'))[0][0]
    is_signed = True
    # study_site = None
