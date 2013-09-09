import factory
from datetime import datetime
from lab_base_model.tests.factories import BaseLabUuidModelFactory


class BaseOrderFactory(BaseLabUuidModelFactory):
    ABSTRACT_FACTORY = True

    order_identifier = factory.Sequence(lambda n: n.rjust(8, '0'))
    order_datetime = datetime.today()
