import factory
from datetime import date, datetime
from bcpp_subject.tests.factories import SubjectVisitFactory
from base_scheduled_model_factory import BaseScheduledModelFactory
from bcpp_subject.models import OutpatientCare


class OutpatientCareFactory(BaseScheduledModelFactory):
    FACTORY_FOR = OutpatientCare

    subject_visit = factory.SubFactory(SubjectVisitFactory)

    report_datetime = datetime.today()
    govt_health_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    dept_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    prvt_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    trad_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    facility_visited = (('Government Clinic/Post', 'Government Primary Health Clinic/Post'), ('Chemist/Pharmacy', 'Chemist/Pharmacy'), ('Hospital Outpatient Department', 'Hospital Outpatient Department (including government and private)'), ('Private Doctor', 'Private Doctor'), ('Traditional or Faith Healer', 'Traditional or Faith Healer'), ('No visit in past 3 months', 'No visit in past 3 months'), ("Don't want to answer", "Don't want to answer"))[0][0]
    care_reason = (('HIV-related care', 'HIV-related care, including TB and other opportunistic infections'), ('Pregnancy', 'Pregnancy-related care, including delivery'), ('Injuries', 'Injuries or accidents'), ('Chronic disease', 'Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness'), ('Other', 'Other'), ("Don't want to answer", "Don't want to answer"))[0][0]
    care_reason_other = factory.Sequence(lambda n: 'care_reason_other{0}'.format(n))
    outpatient_expense = 2.5
    travel_time = (('Under 0.5 hour', 'Under 0.5 hour'), ('0.5 to under 1 hour', '0.5 to under 1 hour'), ('1 to under 2 hours', '1 to under 2 hours'), ('2 to under 3 hours', '2 to under 3 hours'), ('More than 3 hours', 'More than 3 hours'), ("Don't want to answer", "Don't want to answer"))[0][0]
    transport_expense = 2.5
    cost_cover = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    waiting_hours = (('Under 0.5 hour', 'Under 0.5 hour'), ('0.5 to under 1 hour', '0.5 to under 1 hour'), ('1 to under 2 hours', '1 to under 2 hours'), ('2 to under 3 hours', '2 to under 3 hours'), ('More than 3 hours', 'More than 3 hours'), ("Don't want to answer", "Don't want to answer"))[0][0]
