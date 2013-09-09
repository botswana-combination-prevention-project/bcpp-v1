import factory
from base_aliquot_type_factory import BaseAliquotTypeFactory
from lab_aliquot_list.models import AliquotType


class AliquotTypeFactory(BaseAliquotTypeFactory):
    FACTORY_FOR = AliquotType

    dmis_reference = factory.Sequence(lambda n: n)
