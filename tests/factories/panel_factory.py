import factory
from lab_panel.tests.factories import BasePanelFactory
from lab_clinic_api.models import Panel


class PanelFactory(BasePanelFactory):
    FACTORY_FOR = Panel

    panel_type = 'TEST'
    # m2m aliquot_type = factory.SubFactory(AliquotTypeFactory)
