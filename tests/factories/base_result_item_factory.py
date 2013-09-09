import factory
from datetime import datetime
from lab_base_model.tests.factories import BaseLabUuidModelFactory


class BaseResultItemFactory(BaseLabUuidModelFactory):
    ABSTRACT_FACTORY = True

    result_item_value = factory.Sequence(lambda n: '{0}'.format(n))
    result_item_datetime = datetime.today()
    validation_status = 'F'
    receive_identifier = ''
