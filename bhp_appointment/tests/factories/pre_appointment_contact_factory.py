import factory
from datetime import datetime
from bhp_appointment.models import PreAppointmentContact
from appointment_factory import AppointmentFactory
from bhp_base_model.tests.factories import BaseUuidModelFactory


class PreAppointmentContactFactory(BaseUuidModelFactory):
    FACTORY_FOR = PreAppointmentContact

    appointment = factory.SubFactory(AppointmentFactory)
    contact_datetime = datetime.today()
    is_contacted = 'Yes'
    is_confirmed = True
