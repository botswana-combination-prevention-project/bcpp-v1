from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory

from ...models import SubjectRequisition


class SubjectRequisitionFactory(BaseUuidModelFactory):
    FACTORY_FOR = SubjectRequisition

    requisition_datetime = datetime.today()
    drawn_datetime = datetime.today()
