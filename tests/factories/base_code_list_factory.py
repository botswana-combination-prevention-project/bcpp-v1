import factory
from bhp_base_model.tests.factories import BaseModelFactory


class BaseCodeListFactory(BaseModelFactory):
    ABSTRACT_FACTORY = True

    code = factory.Sequence(lambda n: 'CODE{0}'.format(n))
    short_name = factory.Sequence(lambda n: 'SNAME{0}'.format(n))
    long_name = factory.Sequence(lambda n: 'LNAME{0}'.format(n))
