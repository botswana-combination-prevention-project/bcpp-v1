import factory

from datetime import datetime

from bhp066.apps.bcpp_household.models import RepresentativeEligibility

from .household_structure_factory import HouseholdStructureFactory


class RepresentativeEligibilityFactory(factory.DjangoModelFactory):
    class Meta:
        model = RepresentativeEligibility

    household_structure = factory.SubFactory(HouseholdStructureFactory)
    report_datetime = datetime.today()
    aged_over_18 = 'Yes'
    household_residency = 'Yes'
    verbal_script = 'Yes'
