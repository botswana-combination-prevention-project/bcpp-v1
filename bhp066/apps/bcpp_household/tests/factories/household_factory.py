import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Household
from .plot_factory import PlotFactory


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    plot = factory.SubFactory(PlotFactory)
    household_identifier = factory.Sequence(lambda n: '1400011-08{0}'.format(n))