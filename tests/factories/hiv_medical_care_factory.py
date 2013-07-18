import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HivMedicalCare


class HivMedicalCareFactory(BaseUuidModelFactory):
    FACTORY_FOR = HivMedicalCare

    report_datetime = datetime.today()
    first_hiv_care_pos = date.today()
    last_hiv_care_pos = date.today()
    lowest_cd4 = (('0-49', '0-49'), ('50-99', '50-99'), ('100-199', '100-199'), ('200-349', '200-349'), ('350-499', '350-499'), ('500 or more', '500 or more'), ('I am not sure', 'I am not sure'), ("Don't want to answer", "Don't want to answer"))[0][0]
