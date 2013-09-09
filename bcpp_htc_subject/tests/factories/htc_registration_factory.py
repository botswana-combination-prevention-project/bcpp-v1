import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_htc_subject.models import HtcRegistration
from bhp_variables.tests.factories import StudySiteFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp_registration.tests.factories import RegisteredSubjectFactory


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
