import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import HospitalAdmission


class HospitalAdmissionFactory(BaseUuidModelFactory):
    FACTORY_FOR = HospitalAdmission

    report_datetime = datetime.today()
    reason_hospitalized = (('HIV-related care', 'HIV-related care, including TB and other opportunistic infections'), ('Pregnancy', 'Pregnancy-related care, including delivery'), ('Injuries', 'Injuries or accidents'), ('Chronic disease', 'Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness'), ('Other', 'Other'), ("Don't want to answer", "Don't want to answer"))[0][0]
    facility_hospitalized = factory.Sequence(lambda n: 'facility_hospitalized{0}'.format(n))
    nights_hospitalized = 2
    healthcare_expense = 2.5
    travel_hours = (('Under 0.5 hour', 'Under 0.5 hour'), ('0.5 to under 1 hour', '0.5 to under 1 hour'), ('1 to under 2 hours', '1 to under 2 hours'), ('2 to under 3 hours', '2 to under 3 hours'), ('More than 3 hours', 'More than 3 hours'), ("Don't want to answer", "Don't want to answer"))[0][0]
    hospitalization_costs = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
