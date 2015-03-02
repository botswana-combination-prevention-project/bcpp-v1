import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import HouseholdRefusal

from .household_structure_factory import HouseholdStructureFactory


class HouseholdRefusalFactory(BaseUuidModelFactory):
    class Meta:
        model = HouseholdRefusal

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
    reason = 'not_interested'
