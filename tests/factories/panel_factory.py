import factory
from lab_panel.tests.factories import BasePanelFactory
# TODO: fix panel import, chencged here to make the factory work
from lab_panel.models import Panel
from aliquot_factory import AliquotTypeFactory
from lab_panel.tests.factories import PanelGroupFactory


class PanelFactory(BasePanelFactory):
    FACTORY_FOR = Panel

    panel_group = factory.SubFactory(PanelGroupFactory)
    # m2m aliquot_type = factory.SubFactory(AliquotTypeFactory)
