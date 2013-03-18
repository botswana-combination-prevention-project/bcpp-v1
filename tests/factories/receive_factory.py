import factory
from bhp_registration.tests.factories import RegisteredSubjectFactory
from lab_receive.tests.factories import BaseReceiveFactory
from lab_clinic_api.models import Receive


class ReceiveFactory(BaseReceiveFactory):
    FACTORY_FOR = Receive

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
