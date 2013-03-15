import factory
from datetime import datetime
from bhp_registration.factories import RegisteredSubjectFactory
from bhp_visit.factories import VisitDefinitionFactory
from bhp_variables.factories import StudySiteFactory
from bhp_appointment.models import Appointment


class AppointmentFactory(factory.DjangoModelFactory):
    FACTORY_FOR = Appointment

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    best_appt_datetime = datetime.today()
    appt_close_datetime = datetime.today()
    study_site = factory.SubFactory(StudySiteFactory)
    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    visit_instance = 0
    dashboard_type = 'subject'
