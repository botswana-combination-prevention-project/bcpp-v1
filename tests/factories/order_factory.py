import factory
from lab_order.tests.factories import BaseOrderFactory
from lab_clinic_api.models import Order
from aliquot_factory import AliquotFactory
from panel_factory import PanelFactory


class OrderFactory(BaseOrderFactory):
    FACTORY_FOR = Order

    aliquot = factory.SubFactory(AliquotFactory)
    panel = factory.SubFactory(PanelFactory)
