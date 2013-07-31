import factory
from datetime import date, datetime
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bcpp_subject.models import OutpatientCare


class OutpatientCareFactory(BaseUuidModelFactory):
    FACTORY_FOR = OutpatientCare

    report_datetime = datetime.today()
    govt_health_care = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    dept_care = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    prvt_care = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    trad_care = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    facility_visited = (('Government Clinic/Post', u'Government Primary Health Clinic/Post'), ('Chemist/Pharmacy', u'Chemist/Pharmacy'), ('Hospital Outpatient Department', u'Hospital Outpatient Department (including government and private)'), ('Private Doctor', u'Private Doctor'), ('Traditional or Faith Healer', u'Traditional or Faith Healer'), ('No visit in past 3 months', u'No visit in past 3 months'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    care_reason = (('HIV-related care', u'HIV-related care, including TB and other opportunistic infections'), ('Pregnancy', u'Pregnancy-related care, including delivery'), ('Injuries', u'Injuries or accidents'), ('Chronic disease', u'Chronic disease related care, including high blood pressure, diabetes, cancer, mental illness'), ('Other', u'Other'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    care_reason_other = factory.Sequence(lambda n: 'care_reason_other{0}'.format(n))
    outpatient_expense = 2.5
    travel_time = (('Under 0.5 hour', u'Under 0.5 hour'), ('0.5 to under 1 hour', u'0.5 to under 1 hour'), ('1 to under 2 hours', u'1 to under 2 hours'), ('2 to under 3 hours', u'2 to under 3 hours'), ('More than 3 hours', u'More than 3 hours'), ("Don't want to answer", u"Don't want to answer"))[0][0]
    transport_expense = 2.5
    cost_cover = (('Yes', <django.utils.functional.__proxy__ object at 0x101d48f50>), ('No', <django.utils.functional.__proxy__ object at 0x101d48fd0>), ('REF', <django.utils.functional.__proxy__ object at 0x101d52090>))[0][0]
    waiting_hours = (('Under 0.5 hour', u'Under 0.5 hour'), ('0.5 to under 1 hour', u'0.5 to under 1 hour'), ('1 to under 2 hours', u'1 to under 2 hours'), ('2 to under 3 hours', u'2 to under 3 hours'), ('More than 3 hours', u'More than 3 hours'), ("Don't want to answer", u"Don't want to answer"))[0][0]
