import factory

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import IncreasePlotRadius


class PlotFactory(BaseUuidModelFactory):
    FACTORY_FOR = IncreasePlotRadius
