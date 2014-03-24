import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdRefusal
from .household_factory import HouseholdFactory


class HouseholdRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdRefusal

    household = factory.SubFactory(HouseholdFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'