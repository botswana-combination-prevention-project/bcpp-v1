import factory
from edc_lib.bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_household.models import Household
from plot_factory import PlotFactory


class HouseholdFactory(BaseUuidModelFactory):
    FACTORY_FOR = Household

    plot = factory.SubFactory(PlotFactory)
