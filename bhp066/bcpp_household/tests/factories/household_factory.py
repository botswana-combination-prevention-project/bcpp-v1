import factory
from edc.core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import Household
from .plot_factory import PlotFactory


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    plot = factory.SubFactory(PlotFactory)
