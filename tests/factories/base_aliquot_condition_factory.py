

import factory
from lab_base_model.tests.factories import BaseLabListModelFactory


class BaseAliquotConditionFactory(BaseLabListModelFactory):
    ABSTRACT_FACTORY = True

    name = factory.Sequence(lambda n: 'NAME{0}'.format(n))
    short_name = factory.Sequence(lambda n: 'SHORTNAME{0}'.format(n))
