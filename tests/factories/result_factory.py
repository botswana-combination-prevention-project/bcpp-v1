import factory
from lab_result.tests.factories import BaseResultFactory
from lab_clinic_api.models import Result
from order_factory import OrderFactory


class ResultFactory(BaseResultFactory):
    FACTORY_FOR = Result

    order = factory.SubFactory(OrderFactory)
