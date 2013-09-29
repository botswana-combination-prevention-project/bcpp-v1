import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from ..models import HtcSubjectVisit
from bhp_appointment.tests.factories import AppointmentFactory
from bcpp_household_member.tests.factories import HouseholdMemberFactory


class HtcSubjectVisitFactory(BaseUuidModelFactory):
    FACTORY_FOR = HtcSubjectVisit

    appointment = factory.SubFactory(AppointmentFactory)
    report_datetime = datetime.today()
    reason = factory.Sequence(lambda n: 'reason{0}'.format(n))
    info_source = factory.Sequence(lambda n: 'info_source{0}'.format(n))
    info_source_other = factory.Sequence(lambda n: 'info_source_other{0}'.format(n))
    subject_identifier = factory.Sequence(lambda n: 'subject_identifier{0}'.format(n))
    household_member = factory.SubFactory(HouseholdMemberFactory)
