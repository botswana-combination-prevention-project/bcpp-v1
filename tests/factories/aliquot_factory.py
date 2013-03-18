import factory
from lab_aliquot_list.tests.factories import BaseAliquotTypeFactory, BaseAliquotConditionFactory
from lab_aliquot.tests.factories import BaseAliquotFactory
from lab_clinic_api.models import Aliquot, AliquotCondition
from lab_aliquot_list.models import AliquotType
from receive_factory import ReceiveFactory


class AliquotConditionFactory(BaseAliquotConditionFactory):
    FACTORY_FOR = AliquotCondition


class AliquotTypeFactory(BaseAliquotTypeFactory):
    FACTORY_FOR = AliquotType


class AliquotFactory(BaseAliquotFactory):
    FACTORY_FOR = Aliquot

    receive = factory.SubFactory(ReceiveFactory)
