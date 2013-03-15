import factory
from datetime import datetime
from bhp_appointment.factories import AppointmentFactory


class BaseVisitTrackingFactory(factory.DjangoModelFactory):

    appointment = factory.SubFactory(AppointmentFactory)
    report_datetime = datetime.today()
    reason = 'clinic'
    reason_missed = None
    info_source = 'subject'
    comment = None
