from datetime import datetime

import factory
from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import SubjectHtc

from .household_member_factory import HouseholdMemberFactory


class SubjectHtcFactory(BaseUuidModelFactory):

    class Meta:
        model = SubjectHtc

    report_datetime = datetime.today()
    household_member = factory.SubFactory(HouseholdMemberFactory)
    report_datetime = datetime.today()
    offered = 'Yes'
    accepted = 'Yes'
    referred = 'No'
