import factory
from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.core.bhp_variables.tests.factories import StudySiteFactory

from apps.bcpp_subject.tests.factories import SubjectVisitFactory

from ..factories import PanelFactory
from ..factories import AliquotTypeFactory
from ...models import SubjectRequisition



class SubjectRequisitionFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectRequisition

    subject_visit = factory.SubFactory(SubjectVisitFactory)
    aliquot_type = factory.SubFactory(AliquotTypeFactory)
    panel = factory.SubFactory(PanelFactory)
    site = factory.SubFactory(StudySiteFactory)
    requisition_datetime = datetime.today()
    drawn_datetime = datetime.today()
