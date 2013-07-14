import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import HivMedicalCare


class HivMedicalCareFactory(BaseScheduledModelFactory):
    FACTORY_FOR = HivMedicalCare

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    first_hiv_care_pos = date.today()
    last_hiv_care_pos = date.today()
    lowest_cd4 = (('0-49', '0-49'), ('50-99', '50-99'), ('100-199', '100-199'), ('200-349', '200-349'), ('350-499', '350-499'), ('500 or more', '500 or more'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
