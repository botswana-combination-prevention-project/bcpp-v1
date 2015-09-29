import factory

from bhp066.apps.bcpp_household.models import IncreasePlotRadius


class IncreasePlotRadiusFactory(factory.DjangoModelFactory):
    class Meta:
        model = IncreasePlotRadius
