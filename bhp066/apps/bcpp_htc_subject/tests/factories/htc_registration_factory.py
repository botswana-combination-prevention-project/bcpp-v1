import factory
from datetime import datetime
from edc.core.bhp_variables.tests.factories import StudySiteFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.base.model.tests.factories import BaseUuidModelFactory

from bhp066.apps.bcpp_household_member.tests.factories import HouseholdMemberFactory

from ...models import HtcRegistration


class HtcRegistrationFactory(BaseUuidModelFactory):
    FACTORY_FOR = HtcRegistration

    subject_identifier = factory.Sequence(lambda n: 'subject_identifier{0}'.format(n))
    study_site = factory.SubFactory(StudySiteFactory)
    consent_datetime = datetime.today()
    may_store_samples = 'No'
    is_incarcerated = 'No'
    is_literate = 'Yes'
    consent_version_on_entry = 2
    consent_version_recent = 2
    language = (('tn', 'Setswana'), ('en', 'English'))[0][0]
    is_verified = False
    identity = factory.Sequence(lambda n: 'identity{0}'.format(n))
    identity_type = (('OMANG', 'Omang'), ('DRIVERS', "Driver's License"), ('PASSPORT', 'Passport'), ('OMANG_RCPT', 'Omang Receipt'), ('OTHER', 'Other'))[0][0]
    household_member = factory.SubFactory(HouseholdMemberFactory)
    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    report_datetime = datetime.today()
    is_resident = 'Yes'
    citizen = 'Yes'
    omang = factory.Sequence(lambda n: 'omang{0}'.format(n))
