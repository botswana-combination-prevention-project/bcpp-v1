import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdEnumerationRefusal
from .household_factory import HouseholdFactory


class HouseholdEnumerationRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdEnumerationRefusal

    household = factory.SubFactory(HouseholdFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'