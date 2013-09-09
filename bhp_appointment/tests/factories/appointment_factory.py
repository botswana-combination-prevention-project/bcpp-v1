import factory
from datetime import datetime
from bhp_registration.tests.factories import RegisteredSubjectFactory
from bhp_visit.tests.factories import VisitDefinitionFactory
from bhp_variables.tests.factories import StudySiteFactory
from bhp_appointment.models import Appointment
from bhp_base_model.tests.factories import BaseUuidModelFactory


class AppointmentFactory(BaseUuidModelFactory):
    FACTORY_FOR = Appointment

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    appt_datetime = datetime.today()
    best_appt_datetime = datetime.today()
    appt_close_datetime = datetime.today()
    study_site = factory.SubFactory(StudySiteFactory)
    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    visit_instance = '0'
