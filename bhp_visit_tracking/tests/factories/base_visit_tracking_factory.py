import factory
from datetime import datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_appointment.tests.factories import AppointmentFactory


class BaseVisitTrackingFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    appointment = factory.SubFactory(AppointmentFactory)
    report_datetime = datetime.today()
    reason = 'scheduled'
    reason_missed = None
    info_source = 'subject'
