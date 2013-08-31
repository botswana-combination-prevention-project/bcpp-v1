import factory
from datetime import datetime
from lab_base_model.tests.factories import BaseLabUuidModelFactory


class BaseReceiveFactory(BaseLabUuidModelFactory):
    ABSTRACT_FACTORY = True

    receive_identifier = factory.Sequence(lambda n: '{0}'.format(n).rjust(8, '0'))
    requisition_identifier = factory.Sequence(lambda n: '{0}'.format(n).rjust(8, '0'))
    drawn_datetime = datetime.today()
    visit = '1000'
    clinician_initials = 'XXX'
