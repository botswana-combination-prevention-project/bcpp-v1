import factory
from lab_base_model.tests.factories import BaseLabListModelFactory


class BaseAliquotTypeFactory(BaseLabListModelFactory):
    ABSTRACT_FACTORY = True

    alpha_code = factory.Iterator(['AA', 'BB', 'CC', 'DD', 'EE', 'FF', 'GG', 'HH', 'JJ', 'KK', 'LL', 'MM'])
    numeric_code = factory.Iterator(['01', '02', '03', '04', '05', '06', '07', '08' '09', '10', '11', '12'])
    name = factory.Sequence(lambda n: 'Aliquot{0}'.format(n))
