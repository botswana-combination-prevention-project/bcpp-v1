import factory

from datetime import datetime

from bhp066.apps.bcpp_household.models import HouseholdRefusal

from .household_structure_factory import HouseholdStructureFactory


class HouseholdRefusalFactory(factory.DjangoModelFactory):
    class Meta:
        model = HouseholdRefusal

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
    reason = 'not_interested'
