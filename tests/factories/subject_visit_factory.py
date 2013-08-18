import factory
from datetime import datetime
from bcpp_subject.models import SubjectVisit
from bhp_appointment.tests.factories import AppointmentFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory
from bhp_visit_tracking.tests.factories import BaseVisitTrackingFactory


class SubjectVisitFactory(BaseVisitTrackingFactory):
    FACTORY_FOR = SubjectVisit

    appointment = factory.SubFactory(AppointmentFactory)
    report_datetime = datetime.today()
    reason = factory.Sequence(lambda n: 'reason{0}'.format(n))
    info_source = factory.Sequence(lambda n: 'info_source{0}'.format(n))
    info_source_other = factory.Sequence(lambda n: 'info_source_other{0}'.format(n))
    subject_identifier = factory.Sequence(lambda n: 'subject_identifier{0}'.format(n))
    household_member = factory.SubFactory(HouseholdMemberFactory)
