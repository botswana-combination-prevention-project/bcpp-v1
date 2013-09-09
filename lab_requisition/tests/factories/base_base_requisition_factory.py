import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_variables.tests.factories import StudySiteFactory
from lab_clinic_api.tests.factories import PanelFactory
from lab_aliquot_list.tests.factories import AliquotTypeFactory


class BaseBaseRequisitionFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    requisition_identifier = factory.Sequence(lambda n: n.rjust(8, '0'))
    requisition_datetime = datetime.today()
    site = factory.SubFactory(StudySiteFactory)
    aliquot_type = factory.SubFactory(AliquotTypeFactory)
    panel = factory.SubFactory(PanelFactory)
    drawn_datetime = datetime.today()
