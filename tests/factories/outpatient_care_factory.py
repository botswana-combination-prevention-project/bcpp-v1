import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import OutpatientCare


class OutpatientCareFactory(BaseUuidModelFactory):
    FACTORY_FOR = OutpatientCare

    report_datetime = datetime.today()
    govt_health_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    dept_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    prvt_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    trad_care = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    facility_visited = (('Government Clinic/Post', <django.utils.functional.__proxy__ object at 0x103a18e90>), ('Chemist/Pharmacy', <django.utils.functional.__proxy__ object at 0x103a18f10>), ('Hospital Outpatient Department', <django.utils.functional.__proxy__ object at 0x103a18f90>), ('Private Doctor', <django.utils.functional.__proxy__ object at 0x103a1a050>), ('Traditional or Faith Healer', <django.utils.functional.__proxy__ object at 0x103a1a0d0>), ('No visit in past 3 months', <django.utils.functional.__proxy__ object at 0x103a1a150>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1a1d0>))[0][0]
    care_reason = (('HIV-related care', <django.utils.functional.__proxy__ object at 0x103a1a250>), ('Pregnancy', <django.utils.functional.__proxy__ object at 0x103a1a2d0>), ('Injuries', <django.utils.functional.__proxy__ object at 0x103a1a350>), ('Chronic disease', <django.utils.functional.__proxy__ object at 0x103a1a3d0>), ('Other', <django.utils.functional.__proxy__ object at 0x103a1a450>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1a4d0>))[0][0]
    care_reason_other = factory.Sequence(lambda n: 'care_reason_other{0}'.format(n))
    outpatient_expense = 2.5
    travel_time = (('Under 0.5 hour', <django.utils.functional.__proxy__ object at 0x103a1a550>), ('0.5 to under 1 hour', <django.utils.functional.__proxy__ object at 0x103a1a5d0>), ('1 to under 2 hours', <django.utils.functional.__proxy__ object at 0x103a1a650>), ('2 to under 3 hours', <django.utils.functional.__proxy__ object at 0x103a1a6d0>), ('More than 3 hours', <django.utils.functional.__proxy__ object at 0x103a1a750>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1a7d0>))[0][0]
    transport_expense = 2.5
    cost_cover = (('Yes', 'Yes'), ('No', 'No'), ('REF', 'Refused to answer'))[0][0]
    waiting_hours = (('Under 0.5 hour', <django.utils.functional.__proxy__ object at 0x103a1a550>), ('0.5 to under 1 hour', <django.utils.functional.__proxy__ object at 0x103a1a5d0>), ('1 to under 2 hours', <django.utils.functional.__proxy__ object at 0x103a1a650>), ('2 to under 3 hours', <django.utils.functional.__proxy__ object at 0x103a1a6d0>), ('More than 3 hours', <django.utils.functional.__proxy__ object at 0x103a1a750>), ("Don't want to answer", <django.utils.functional.__proxy__ object at 0x103a1a7d0>))[0][0]
