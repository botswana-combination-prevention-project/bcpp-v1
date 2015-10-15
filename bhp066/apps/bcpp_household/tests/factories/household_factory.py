import factory

from bhp066.apps.bcpp_household.models import Household

from .plot_factory import PlotFactory


class HouseholdFactory(factory.DjangoModelFactory):
    class Meta:
        model = Household

    plot = factory.SubFactory(PlotFactory)
    household_identifier = factory.Sequence(lambda n: '1400011-08{0}'.format(n))
