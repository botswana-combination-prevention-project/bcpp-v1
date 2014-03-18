import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import HouseholdRefusal
from .plot_factory import PlotFactory


class HouseholdRefusalFactory(BaseUuidModelFactory):
    FACTORY_FOR = HouseholdRefusal

    household = factory.SubFactory(PlotFactory)
    report_datetime = datetime.now()
    reason = 'Does not have time'