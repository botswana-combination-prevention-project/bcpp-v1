import factory
from datetime import date, datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp_household_member.tests.factories import HouseholdMemberFactory
from ...models import CallList


class CallListFactory(BaseUuidModelFactory):
    FACTORY_FOR = CallList

    household_member = factory.SubFactory(HouseholdMemberFactory)
    community = 'otse'
    subject_identifier = factory.Sequence(lambda n: '066-21444678-{0}'.format(n))
    first_name = factory.Sequence(lambda n: 'ONIZA{0}'.format(n))
    initials = factory.Sequence(lambda n: 'OP{0}'.format(n))
    gender = 'F'
    consent_datetime = datetime.today()
    call_attempts = 1
    call_status = 'Open'